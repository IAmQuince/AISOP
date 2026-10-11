#!/usr/bin/env python
"""Edition audit: tree-level checks for the entry layer and the single-source rules.

Checks the tree you are standing in (the repository, or an unzipped edition):
references resolve; AGENTS.md size, identity and status; the card's rules-block
cap; pointer files; card report labels equal the template's; every header's
package_id matches config; warnings for a missing cold-agent log and for
superseded documents outside tier 3. Ownership: docs/166 section 11.
"""
from __future__ import print_function

import re
import sys
import time

from _aisop_common import PACKAGE_ID_TOKEN, ROOT, current_edition, find_region, glob_match, split_frontmatter
from _aisop_editions import Tree, config_for, rules_block, unresolved_references

REPORT = ROOT / 'reports' / 'edition_audit_report.txt'


class Audit(object):
    def __init__(self):
        self.lines, self.errors, self.warnings = [], [], []

    def section(self, title):
        self.lines += ['', title, '-' * 72]

    def check(self, ok, msg):
        self.lines.append('%s %s' % ('PASS' if ok else 'FAIL', msg))
        if not ok:
            self.errors.append(msg)

    def warn(self, msg):
        self.lines.append('WARN ' + msg)
        self.warnings.append(msg)


def example_roots(cfg):
    return [r.rstrip('/') for r in cfg.get('example_packages', [])]


def in_example(rel, roots):
    return any(rel.startswith(r + '/') for r in roots)


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def check_references(audit, tree, cfg, eds):
    """TEST-LINK-001 (tree): every link and backticked repo path resolves here."""
    audit.section('REFERENCES IN THIS TREE (TEST-LINK-001)')
    edition = current_edition(tree.root)
    problems = unresolved_references(tree, edition, example_roots(cfg), eds.data.get('link_check'))
    for rel, line, target in problems:
        audit.check(False, '%s:%d cites %r, which does not exist in this tree' % (rel, line, target))
    if not problems:
        audit.check(True, 'every link and backticked repo path resolves (%s tree)' % edition)


def check_agents_file(audit, tree, cfg, eds):
    """TEST-ENTRY-001."""
    audit.section('AGENTS.md (TEST-ENTRY-001)')
    spec = eds.data['agents_file']
    rel = spec['path']
    if rel not in tree.files:
        audit.check(False, '%s is missing' % rel)
        return
    size, budget = len(tree.files[rel]), spec['budget_bytes']
    audit.check(size <= budget, '%s is %d of %d bytes (headroom %d)' % (rel, size, budget, budget - size))
    header = tree.header(rel)
    audit.check(header.get('package_id') == cfg['package_id'] and header.get('version') == cfg['version'],
                'header package_id/version equal config (%s %s)' % (cfg['package_id'], cfg['version']))
    audit.check(header.get('normative_status') == 'Normative', 'normative_status is Normative')
    _, body = split_frontmatter(tree.text(rel))
    others = sorted(set(PACKAGE_ID_TOKEN.findall(body)))
    audit.check(not others, 'body names no package_id-shaped token (found: %s)' % (others or 'none'))
    for region in ('rules', 'commands'):
        audit.check(find_region(tree.text(rel), region) is not None, 'GENERATED region %r present' % region)
    for phrase in ('ORIENT', 'APPLY', 'MODIFY-AISOP', 'DOMAIN-LOOKUP', 'docs/005_PRODUCT_REQUIREMENTS.md'):
        audit.check(phrase in body, 'states %s' % phrase)


def check_card(audit, tree, eds):
    """TEST-ED-003: rules-block cap and the card's report labels equal the template's."""
    audit.section('CARD (TEST-ED-003)')
    card = eds.data['card']
    source = card['source']
    if source not in tree.files:
        audit.check(False, '%s is missing' % source)
        return
    text = tree.text(source)
    block = rules_block(text).encode('utf-8')
    audit.check(len(block) <= card['rules_block_budget_bytes'],
                'rules block is %d of %d bytes' % (len(block), card['rules_block_budget_bytes']))
    audit.check(tree.header(source).get('normative_status') == 'Normative', '%s is Normative' % source)
    template = 'templates/FINAL_PACKAGE_REPORT_TEMPLATE.md'
    if template in tree.files:
        card_labels = report_labels(text, '## Final package report')
        tpl_labels = report_labels(tree.text(template), '## Report')
        audit.check(card_labels == tpl_labels and len(card_labels) == 15,
                    'card report labels equal %s (%d labels)' % (template, len(tpl_labels)))


def report_labels(text, heading):
    """Labels of the first fenced block after `heading`: the text before each line's first colon."""
    start = text.find(heading)
    if start == -1:
        return []
    block = re.search(r'```text\n(.*?)```', text[start:], re.DOTALL)
    if not block:
        return []
    return [line.split(':', 1)[0].strip() for line in block.group(1).splitlines() if ':' in line]


def check_pointers(audit, tree, eds):
    """TEST-ENTRY-002."""
    audit.section('POINTER FILES (TEST-ENTRY-002)')
    budget = eds.data['pointer_budget_bytes']
    for pointer in eds.data['pointer_files']:
        rel = pointer['path']
        if rel not in tree.files:
            audit.check(False, '%s is missing (pointer for %s)' % (rel, pointer['tool']))
            continue
        audit.check(len(tree.files[rel]) <= budget, '%s is %d of %d bytes' % (rel, len(tree.files[rel]), budget))
        audit.check(bool(tree.header(rel)), '%s has a document-control header' % rel)
        audit.check('AGENTS.md' in tree.text(rel), '%s names AGENTS.md' % rel)


def check_package_ids(audit, tree, cfg):
    """Every header package_id equals config, except inside registered example packages."""
    audit.section('PACKAGE IDENTITY')
    roots = example_roots(cfg)
    wrong = [(rel, tree.header(rel).get('package_id')) for rel in tree.documents()
             if not in_example(rel, roots) and tree.header(rel).get('package_id') != cfg['package_id']]
    for rel, pid in wrong:
        audit.check(False, '%s has package_id %r, config says %r' % (rel, pid, cfg['package_id']))
    if not wrong:
        audit.check(True, 'every header package_id equals %s' % cfg['package_id'])


def check_warnings(audit, tree, cfg, eds):
    audit.section('WARNINGS')
    log = eds.data['cold_agent_log'].format(package_id=cfg['package_id'])
    if log in tree.files:
        audit.lines.append('PASS cold-agent log present: %s' % log)
    else:
        audit.warn('no cold-agent log for %s (%s); run TEST-ENTRY-004 before release' % (cfg['package_id'], log))
    for rel in tree.documents():
        status = tree.header(rel).get('status', '')
        if status in ('Superseded', 'Rejected', 'SUPERSEDED', 'REJECTED') and tree.tier(rel) != 3:
            audit.warn('%s is %s but tier %d; superseded records belong in tier 3' % (rel, status, tree.tier(rel)))


# ---------------------------------------------------------------------------
# Phase 2: templates, IDs, glossary, size caps
# ---------------------------------------------------------------------------

ID_FAMILY = re.compile(r'\b([A-Z][A-Z0-9]+)-(?:[A-Z0-9]+-)*(?:\d+|N{2,}|X{2,})\b')
CONCRETE_IDS = {
    'REQ': (re.compile(r'\bREQ-[A-Z]+-\d{3}\b'), 'docs/005_PRODUCT_REQUIREMENTS.md'),
    'FEAT': (re.compile(r'\bFEAT-\d{3}\b'), 'FEATURE_INVENTORY.md'),
    'TEST': (re.compile(r'\bTEST-[A-Z]+-\d{3}\b'), 'ACCEPTANCE_TEST_PLAN.md'),
}


def h2_list(text):
    _, body = split_frontmatter(text)
    in_fence, heads = False, []
    for line in body.splitlines():
        if line.startswith('```'):
            in_fence = not in_fence
        elif not in_fence and line.startswith('## '):
            heads.append(line[3:].strip())
    return heads


def required_sections(text):
    """{template path: [section titles]} from a '## Required sections' block."""
    result, current, inside = {}, None, False
    for line in text.splitlines():
        if line.startswith('## '):
            inside = line.strip() == '## Required sections'
            current = None
        elif inside and line.startswith('### '):
            current = line[4:].strip()
            result[current] = []
        elif inside and current and line.startswith('- '):
            result[current].append(line[2:].strip())
    return result


def check_templates(audit, tree):
    """TEST-TPL-001: derived_from resolves, heading parity, placeholder IDs only."""
    audit.section('TEMPLATES (TEST-TPL-001)')
    by_id = {tree.header(rel).get('document_id'): rel for rel in tree.documents()}
    templates = sorted(rel for rel in tree.documents() if rel.startswith('templates/'))
    for rel in templates:
        derived = tree.header(rel).get('derived_from')
        if derived:
            sop = by_id.get(derived)
            audit.check(sop is not None, '%s derived_from %s resolves%s' % (rel, derived, ' to %s' % sop if sop else ''))
            if sop:
                wanted = required_sections(tree.text(sop)).get(rel)
                if wanted is not None:
                    have = h2_list(tree.text(rel))
                    audit.check(have == wanted, '%s headings equal the Required sections in %s (%d sections)'
                                % (rel, sop, len(wanted)))
        text = tree.text(rel)
        concrete = sorted(set(m.group(0) for pattern, _ in CONCRETE_IDS.values() for m in pattern.finditer(text)))
        audit.check(not concrete, '%s uses placeholder IDs only (found: %s)' % (rel, ', '.join(concrete) or 'none'))
    for sop in tree.documents():
        for listed in required_sections(tree.text(sop)):
            audit.check(listed in tree.files, '%s lists Required sections for %s, which exists' % (sop, listed))


def check_id_citations(audit, tree, cfg):
    """Every REQ/FEAT/TEST ID cited in a tier 0-1 document exists where it is defined."""
    audit.section('ID CITATIONS IN TIER 0-1 DOCUMENTS')
    roots = example_roots(cfg)
    defined = {fam: set(pat.findall(tree.text(src))) if src in tree.files else None
               for fam, (pat, src) in CONCRETE_IDS.items()}
    problems = 0
    for rel in tree.documents():
        if tree.tier(rel) > 1 or rel.startswith('templates/') or in_example(rel, roots):
            continue
        for fam, (pattern, src) in CONCRETE_IDS.items():
            if defined[fam] is None:
                continue
            for cited in sorted(set(pattern.findall(tree.text(rel))) - defined[fam]):
                audit.check(False, '%s cites %s, which %s does not define' % (rel, cited, src))
                problems += 1
    if not problems:
        audit.check(True, 'every cited REQ/FEAT/TEST ID exists')


def check_glossary(audit, tree, cfg, eds):
    """TEST-BEG-001 (glossary part): every ID family in tiers 0-2 and every seeded term is defined."""
    audit.section('GLOSSARY (TEST-BEG-001)')
    spec = eds.data.get('glossary', {})
    path = spec.get('path')
    if not path or path not in tree.files:
        audit.check(False, 'glossary %s is missing' % path)
        return
    glossary = tree.text(path)
    roots = example_roots(cfg)
    families = {}
    for rel in tree.documents():
        if tree.tier(rel) > 2 or in_example(rel, roots) or rel == path:
            continue
        for match in ID_FAMILY.finditer(tree.text(rel)):
            families.setdefault(match.group(1), rel)
    families = {f: r for f, r in families.items() if f not in spec.get('ignore_families', [])}
    missing = sorted(f for f in families if '`%s-`' % f not in glossary)
    for fam in missing:
        audit.check(False, 'ID family %s- (used in %s) is not in %s' % (fam, families[fam], path))
    if not missing:
        audit.check(True, '%d ID families defined' % len(families))
    lowered = glossary.lower()
    terms = [t for t in spec.get('terms', []) if '**%s**' % t.lower() not in lowered]
    for term in terms:
        audit.check(False, 'seeded term %r is not a bold glossary entry' % term)
    if not terms:
        audit.check(True, '%d seeded terms defined' % len(spec.get('terms', [])))


def check_size_caps(audit, tree, eds):
    """Per-document and per-folder byte caps from config/editions.json."""
    audit.section('SIZE CAPS')
    for cap in eds.data.get('size_caps', []):
        members = [rel for rel in tree.files if glob_match(cap['glob'], rel) and rel not in cap.get('exclude', [])]
        if not members:
            continue
        if cap.get('mode') == 'total':
            total = sum(len(tree.files[rel]) for rel in members)
            audit.check(total <= cap['max_bytes'], '%s total %d of %d bytes' % (cap['glob'], total, cap['max_bytes']))
        else:
            for rel in members:
                size = len(tree.files[rel])
                audit.check(size <= cap['max_bytes'], '%s %d of %d bytes' % (rel, size, cap['max_bytes']))


def main():
    cfg, eds = config_for()
    tree = Tree.from_disk()
    audit = Audit()
    audit.lines += ['EDITION AUDIT REPORT', '=' * 72, 'timestamp: %s' % time.strftime('%Y-%m-%d %H:%M:%S'),
                    'package_root: %s' % ROOT, 'edition: %s' % current_edition()]
    check_references(audit, tree, cfg, eds)
    check_agents_file(audit, tree, cfg, eds)
    check_card(audit, tree, eds)
    check_pointers(audit, tree, eds)
    check_package_ids(audit, tree, cfg)
    check_templates(audit, tree)
    check_id_citations(audit, tree, cfg)
    check_glossary(audit, tree, cfg, eds)
    check_size_caps(audit, tree, eds)
    check_warnings(audit, tree, cfg, eds)
    audit.lines += ['', 'SUMMARY', '-' * 72, 'SUMMARY: %s' % ('FAIL' if audit.errors else 'PASS')]
    audit.lines += ['ERROR: %s' % e for e in audit.errors]
    audit.lines += ['WARNING: %s' % w for w in audit.warnings]
    text = '\n'.join(audit.lines) + '\n'
    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text(text, encoding='utf-8')
    print(text)
    return 1 if audit.errors else 0


if __name__ == '__main__':
    sys.exit(main())
