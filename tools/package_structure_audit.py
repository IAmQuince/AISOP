#!/usr/bin/env python
from __future__ import print_function
import os
import re
import sys
import json
import time
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = PACKAGE_ROOT / 'reports'
REPORT_PATH = REPORT_DIR / 'package_structure_audit_report.txt'

REQUIRED_ROOT_FILES = [
    'README.md',
    'README_START_HERE.md',
    'CHANGELOG.md',
    'FEATURE_INVENTORY.md',
    'ACCEPTANCE_TEST_PLAN.md',
    'KNOWN_LIMITATIONS.md',
    'WORKPLAN_CURRENT_RUN.md',
    'PACKAGE_MANIFEST.md',
    'REQUIREMENTS_TRACEABILITY_MATRIX.md',
    'CONTRIBUTING.md',
    'SECURITY.md',
    'SAFETY.md',
    'LICENSE_DECISION_REQUIRED.md',
]

REQUIRED_DIRS = ['docs', 'tools', 'tests', 'reports', 'src', 'requirements', 'config', '.github']
REQUIRED_FRONTMATTER_KEYS = [
    'document_id', 'title', 'version', 'revision', 'status',
    'last_updated', 'package_id', 'machine_reference_prefix', 'normative_status'
]
PERSONAL_REFERENCE_PATTERNS = [
    r'\bScott\b',
    r'Fackler',
    r'ScottXY',
    r'C:\\Users\\Scott',
]


def read_text(path):
    try:
        return path.read_text(encoding='utf-8')
    except TypeError:
        return path.read_text()
    except Exception:
        with open(str(path), 'r') as f:
            return f.read()


def has_frontmatter(text):
    return text.startswith('---\n') and '\n---\n' in text[4:1200]


def parse_frontmatter(text):
    if not has_frontmatter(text):
        return {}
    block = text.split('\n---\n', 1)[0].strip('-\n')
    result = {}
    for line in block.splitlines():
        if ':' in line:
            key, value = line.split(':', 1)
            result[key.strip()] = value.strip().strip('"')
    return result


def main():
    REPORT_DIR.mkdir(exist_ok=True)
    lines = []
    errors = []
    warnings = []

    lines.append('PACKAGE STRUCTURE AUDIT REPORT')
    lines.append('=' * 72)
    lines.append('timestamp: %s' % time.strftime('%Y-%m-%d %H:%M:%S'))
    lines.append('package_root: %s' % PACKAGE_ROOT)
    lines.append('')

    lines.append('REQUIRED ROOT FILES')
    lines.append('-' * 72)
    for name in REQUIRED_ROOT_FILES:
        path = PACKAGE_ROOT / name
        if path.exists() and path.stat().st_size > 0:
            lines.append('PASS %s' % name)
        else:
            msg = 'FAIL missing or empty root file: %s' % name
            lines.append(msg)
            errors.append(msg)

    lines.append('')
    lines.append('REQUIRED DIRECTORIES')
    lines.append('-' * 72)
    for name in REQUIRED_DIRS:
        path = PACKAGE_ROOT / name
        if path.is_dir():
            lines.append('PASS %s/' % name)
        else:
            msg = 'FAIL missing directory: %s/' % name
            lines.append(msg)
            errors.append(msg)

    lines.append('')
    lines.append('MARKDOWN DOCUMENT CONTROL')
    lines.append('-' * 72)
    doc_ids = {}
    for path in sorted(PACKAGE_ROOT.rglob('*.md')):
        rel = path.relative_to(PACKAGE_ROOT).as_posix()
        if rel.startswith('.github/'):
            continue
        text = read_text(path)
        fm = parse_frontmatter(text)
        if not fm:
            msg = 'FAIL no frontmatter: %s' % rel
            lines.append(msg)
            errors.append(msg)
            continue
        missing = [k for k in REQUIRED_FRONTMATTER_KEYS if k not in fm or not fm[k]]
        if missing:
            msg = 'FAIL frontmatter missing %s: %s' % (missing, rel)
            lines.append(msg)
            errors.append(msg)
        else:
            doc_id = fm['document_id']
            if doc_id in doc_ids:
                msg = 'FAIL duplicate document_id %s in %s and %s' % (doc_id, rel, doc_ids[doc_id])
                lines.append(msg)
                errors.append(msg)
            else:
                doc_ids[doc_id] = rel
                lines.append('PASS %s -> %s' % (rel, doc_id))

    lines.append('')
    lines.append('REQUIREMENT CATALOG')
    lines.append('-' * 72)
    req_json = PACKAGE_ROOT / 'requirements' / 'requirements_catalog.json'
    req_doc = PACKAGE_ROOT / 'docs' / '005_PRODUCT_REQUIREMENTS.md'
    if req_json.exists() and req_doc.exists():
        try:
            data = json.loads(read_text(req_json))
            reqs = data.get('requirements', [])
            ids = [r.get('id') for r in reqs]
            if not reqs:
                errors.append('FAIL no requirements in requirements_catalog.json')
                lines.append('FAIL no requirements in requirements_catalog.json')
            elif len(ids) != len(set(ids)):
                errors.append('FAIL duplicate requirement IDs in requirements_catalog.json')
                lines.append('FAIL duplicate requirement IDs in requirements_catalog.json')
            else:
                lines.append('PASS requirements_catalog.json contains %d requirements' % len(reqs))
            doc_text = read_text(req_doc)
            for rid in ids:
                if rid and rid not in doc_text:
                    msg = 'FAIL requirement ID in JSON missing from doc: %s' % rid
                    lines.append(msg)
                    errors.append(msg)
        except Exception as exc:
            msg = 'FAIL requirement catalog parse error: %r' % exc
            lines.append(msg)
            errors.append(msg)
    else:
        msg = 'FAIL missing requirement catalog JSON or product requirements doc'
        lines.append(msg)
        errors.append(msg)

    lines.append('')
    lines.append('FEATURE AND TEST IDS')
    lines.append('-' * 72)
    feature_text = read_text(PACKAGE_ROOT / 'FEATURE_INVENTORY.md') if (PACKAGE_ROOT / 'FEATURE_INVENTORY.md').exists() else ''
    test_text = read_text(PACKAGE_ROOT / 'ACCEPTANCE_TEST_PLAN.md') if (PACKAGE_ROOT / 'ACCEPTANCE_TEST_PLAN.md').exists() else ''
    feat_ids = re.findall(r'(?m)^(FEAT-\d+)\b', feature_text)
    test_ids = re.findall(r'(?m)^(TEST-[A-Z]+-\d+)\b', test_text)
    if feat_ids:
        lines.append('PASS feature IDs found: %d' % len(feat_ids))
    else:
        msg = 'FAIL no FEAT-* IDs found in FEATURE_INVENTORY.md'
        lines.append(msg); errors.append(msg)
    if test_ids:
        lines.append('PASS acceptance test IDs found: %d' % len(test_ids))
    else:
        msg = 'FAIL no TEST-* IDs found in ACCEPTANCE_TEST_PLAN.md'
        lines.append(msg); errors.append(msg)

    lines.append('')
    lines.append('PERSONAL REFERENCE SCAN')
    lines.append('-' * 72)
    hits = []
    for path in sorted(PACKAGE_ROOT.rglob('*.md')):
        rel = path.relative_to(PACKAGE_ROOT).as_posix()
        if rel.startswith('.github/'):
            continue
        text = read_text(path)
        for pat in PERSONAL_REFERENCE_PATTERNS:
            if re.search(pat, text):
                hits.append((rel, pat))
    if hits:
        for rel, pat in hits:
            msg = 'FAIL personal reference pattern %r in %s' % (pat, rel)
            lines.append(msg)
            errors.append(msg)
    else:
        lines.append('PASS no configured personal-reference patterns found')

    lines.append('')
    lines.append('SUMMARY')
    lines.append('-' * 72)
    if errors:
        lines.append('SUMMARY: FAIL')
        for e in errors:
            lines.append('ERROR: %s' % e)
    else:
        lines.append('SUMMARY: PASS')
    if warnings:
        for w in warnings:
            lines.append('WARNING: %s' % w)

    report = '\n'.join(lines) + '\n'
    REPORT_PATH.write_text(report, encoding='utf-8')
    print(report)
    return 1 if errors else 0

if __name__ == '__main__':
    sys.exit(main())
