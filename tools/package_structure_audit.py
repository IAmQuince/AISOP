#!/usr/bin/env python
"""Package structure audit: required files and folders, document-control headers,
requirement and ID presence, code-fence parity, and the personal-reference scan.

Lists come from config/package_metadata.json. The walk is the shared
git-ignore-aware walk, so a local USER_PROFILE.md or dist/ is never audited.
"""
from __future__ import print_function

import json
import re
import sys
import time

from _aisop_common import ROOT, current_edition, iter_package_files, load_config, parse_frontmatter, read_text, rel_posix

PACKAGE_ROOT = ROOT
REPORT_PATH = ROOT / 'reports' / 'package_structure_audit_report.txt'

REQUIRED_FRONTMATTER_KEYS = [
    'document_id', 'title', 'version', 'revision', 'status',
    'last_updated', 'package_id', 'machine_reference_prefix', 'normative_status',
    'tier', 'summary',
]
SUMMARY_MAX = 200
PERSONAL_REFERENCE_PATTERNS = [
    r'\bScott\b',
    r'Fackler',
    r'ScottXY',
    r'C:\\Users\\Scott',
]
# Third-person descriptions of a specific user (REQ-PROF-001). Operating
# instructions address the AI in the second person; anything personal belongs
# in a local, git-ignored USER_PROFILE.md built from the profile template.
PROFILE_PHRASE_PATTERNS = [
    r'\b(He|She) (often|usually|frequently|prefers|cares|works|values|strongly|dislikes|is an?)\b',
    r'(?i)\bthe user (is an?|strongly|prefers|dislikes|values|has been|cares about)\b',
    r'\bTreat (him|her) as\b',
    r'(?i)\b(his|her) (background|preferences|working context)\b',
]


class Audit(object):
    def __init__(self):
        self.lines, self.errors, self.warnings = [], [], []

    def section(self, title):
        self.lines += ['', title, '-' * 72]

    def ok(self, msg):
        self.lines.append('PASS ' + msg)

    def fail(self, msg):
        self.lines.append('FAIL ' + msg)
        self.errors.append('FAIL ' + msg)

    def warn(self, msg):
        self.lines.append('WARN ' + msg)
        self.warnings.append(msg)


def markdown_files():
    """Tracked-style Markdown files outside .github/ (git-ignored files skipped)."""
    return [p for p in iter_package_files() if p.suffix == '.md' and not rel_posix(p).startswith('.github/')]


def check_required(audit, cfg):
    audit.section('REQUIRED ROOT FILES')
    for name in cfg.get('required_root_files', []):
        path = ROOT / name
        if path.is_file() and path.stat().st_size > 0:
            audit.ok(name)
        else:
            audit.fail('missing or empty root file: %s' % name)
    audit.section('REQUIRED DIRECTORIES')
    for name in cfg.get('required_directories', []):
        if (ROOT / name).is_dir():
            audit.ok('%s/' % name)
        else:
            audit.fail('missing directory: %s/' % name)


def check_headers(audit):
    """TEST-DOC-001 and TEST-ED-001: complete headers, valid tier, short summary, unique document_id."""
    audit.section('MARKDOWN DOCUMENT CONTROL')
    doc_ids = {}
    for path in markdown_files():
        rel = rel_posix(path)
        fm = parse_frontmatter(read_text(path))
        if not fm:
            audit.fail('no frontmatter: %s' % rel)
            continue
        missing = [k for k in REQUIRED_FRONTMATTER_KEYS if not fm.get(k)]
        if missing:
            audit.fail('frontmatter missing %s: %s' % (missing, rel))
            continue
        if fm['tier'] not in ('0', '1', '2', '3'):
            audit.fail('tier must be 0-3, found %r: %s' % (fm['tier'], rel))
        if len(fm['summary']) > SUMMARY_MAX:
            audit.fail('summary longer than %d characters: %s' % (SUMMARY_MAX, rel))
        doc_id = fm['document_id']
        if doc_id in doc_ids:
            audit.fail('duplicate document_id %s in %s and %s' % (doc_id, rel, doc_ids[doc_id]))
        else:
            doc_ids[doc_id] = rel
            audit.ok('%s -> %s (tier %s)' % (rel, doc_id, fm['tier']))


def check_requirements(audit):
    audit.section('REQUIREMENT CATALOG')
    req_json = ROOT / 'requirements' / 'requirements_catalog.json'
    req_doc = ROOT / 'docs' / '005_PRODUCT_REQUIREMENTS.md'
    if not (req_json.exists() and req_doc.exists()):
        audit.fail('missing requirement catalog JSON or product requirements doc')
        return
    try:
        reqs = json.loads(read_text(req_json)).get('requirements', [])
    except ValueError as exc:
        audit.fail('requirement catalog parse error: %r' % exc)
        return
    ids = [r.get('id') for r in reqs]
    if not reqs:
        audit.fail('no requirements in requirements_catalog.json')
    elif len(ids) != len(set(ids)):
        audit.fail('duplicate requirement IDs in requirements_catalog.json')
    else:
        audit.ok('requirements_catalog.json contains %d requirements' % len(reqs))
    doc_text = read_text(req_doc)
    for rid in ids:
        if rid and rid not in doc_text:
            audit.fail('requirement ID in JSON missing from doc: %s' % rid)


def check_feature_and_test_ids(audit):
    audit.section('FEATURE AND TEST IDS')
    feature_path, test_path = ROOT / 'FEATURE_INVENTORY.md', ROOT / 'ACCEPTANCE_TEST_PLAN.md'
    feat_ids = re.findall(r'(?m)^(FEAT-\d+)\b', read_text(feature_path)) if feature_path.exists() else []
    test_ids = re.findall(r'(?m)^(TEST-[A-Z]+-\d+)\b', read_text(test_path)) if test_path.exists() else []
    if feat_ids:
        audit.ok('feature IDs found: %d' % len(feat_ids))
    else:
        audit.fail('no FEAT-* IDs found in FEATURE_INVENTORY.md')
    if test_ids:
        audit.ok('acceptance test IDs found: %d' % len(test_ids))
    else:
        audit.fail('no TEST-* IDs found in ACCEPTANCE_TEST_PLAN.md')


def fence_count(text):
    return sum(1 for line in text.splitlines() if line.startswith('```'))


def check_fence_parity(audit, cfg):
    """TEST-DOC-004: even fence-line count; config lists known Phase 5 exceptions (WARN)."""
    audit.section('CODE FENCE PARITY (REQ-DOC-004)')
    pending = set(cfg.get('fence_parity_pending', []))
    present = set()
    odd = []
    for path in markdown_files():
        rel = rel_posix(path)
        present.add(rel)
        count = fence_count(read_text(path))
        if count % 2 == 0:
            continue
        odd.append(rel)
        if rel in pending:
            audit.warn('unbalanced code fences (%d fence lines) in %s; listed in fence_parity_pending until re-fenced'
                       % (count, rel))
        else:
            audit.fail('unbalanced code fences (%d fence lines) in %s' % (count, rel))
    for rel in sorted((pending & present) - set(odd)):
        audit.fail('%s is balanced now; remove it from fence_parity_pending in config' % rel)
    if not odd:
        audit.ok('every Markdown file has balanced code fences')


def check_personal_references(audit):
    """TEST-GEN-001 and TEST-PROF-001."""
    audit.section('PERSONAL REFERENCE SCAN')
    hits = []
    for path in markdown_files():
        text = read_text(path)
        for pat in PERSONAL_REFERENCE_PATTERNS + PROFILE_PHRASE_PATTERNS:
            if re.search(pat, text):
                hits.append((rel_posix(path), pat))
    for rel, pat in hits:
        audit.fail('personal reference pattern %r in %s' % (pat, rel))
    if not hits:
        audit.ok('no configured personal-reference or profile-phrase patterns found')


def main():
    cfg = load_config()
    audit = Audit()
    audit.lines += ['PACKAGE STRUCTURE AUDIT REPORT', '=' * 72,
                    'timestamp: %s' % time.strftime('%Y-%m-%d %H:%M:%S'),
                    'package_root: %s' % ROOT, 'edition: %s' % current_edition()]
    check_required(audit, cfg)
    check_headers(audit)
    check_requirements(audit)
    check_feature_and_test_ids(audit)
    check_fence_parity(audit, cfg)
    check_personal_references(audit)
    audit.lines += ['', 'SUMMARY', '-' * 72, 'SUMMARY: %s' % ('FAIL' if audit.errors else 'PASS')]
    audit.lines += ['ERROR: %s' % e for e in audit.errors]
    audit.lines += ['WARNING: %s' % w for w in audit.warnings]
    report = '\n'.join(audit.lines) + '\n'
    REPORT_PATH.parent.mkdir(exist_ok=True)
    REPORT_PATH.write_text(report, encoding='utf-8')
    print(report)
    return 1 if audit.errors else 0


if __name__ == '__main__':
    sys.exit(main())
