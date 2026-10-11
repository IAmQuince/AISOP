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

from _aisop_common import PACKAGE_ID_TOKEN, ROOT, current_edition, find_region, split_frontmatter
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
