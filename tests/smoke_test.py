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
REPORT_PATH = REPORT_DIR / 'smoke_test_report.txt'


def read_text(path):
    return path.read_text(encoding='utf-8')


def main():
    REPORT_DIR.mkdir(exist_ok=True)
    lines = []
    failures = []
    lines.append('PACKAGE SMOKE TEST REPORT')
    lines.append('=' * 72)
    lines.append('timestamp: %s' % time.strftime('%Y-%m-%d %H:%M:%S'))
    lines.append('python: %s' % sys.version)
    lines.append('package_root: %s' % PACKAGE_ROOT)
    lines.append('')

    checks = [
        ('README exists', PACKAGE_ROOT / 'README_START_HERE.md'),
        ('Product requirements exists', PACKAGE_ROOT / 'docs' / '005_PRODUCT_REQUIREMENTS.md'),
        ('Feature inventory exists', PACKAGE_ROOT / 'FEATURE_INVENTORY.md'),
        ('Acceptance test plan exists', PACKAGE_ROOT / 'ACCEPTANCE_TEST_PLAN.md'),
        ('Requirement catalog exists', PACKAGE_ROOT / 'requirements' / 'requirements_catalog.json'),
    ]
    for label, path in checks:
        if path.exists() and path.stat().st_size > 0:
            lines.append('PASS %s: %s' % (label, path.relative_to(PACKAGE_ROOT)))
        else:
            msg = 'FAIL %s: %s' % (label, path.relative_to(PACKAGE_ROOT))
            lines.append(msg); failures.append(msg)

    try:
        data = json.loads(read_text(PACKAGE_ROOT / 'requirements' / 'requirements_catalog.json'))
        reqs = data.get('requirements', [])
        lines.append('PASS loaded requirement catalog with %d entries' % len(reqs))
        if len(reqs) < 5:
            failures.append('Requirement catalog has too few entries')
    except Exception as exc:
        msg = 'FAIL could not load requirement catalog: %r' % exc
        lines.append(msg); failures.append(msg)

    try:
        feat_text = read_text(PACKAGE_ROOT / 'FEATURE_INVENTORY.md')
        feats = re.findall(r'(?m)^FEAT-\d+\b', feat_text)
        lines.append('PASS feature IDs counted: %d' % len(feats))
        if len(feats) < 5:
            failures.append('Feature inventory has too few FEAT IDs')
    except Exception as exc:
        msg = 'FAIL feature inventory read failed: %r' % exc
        lines.append(msg); failures.append(msg)

    try:
        test_text = read_text(PACKAGE_ROOT / 'ACCEPTANCE_TEST_PLAN.md')
        tests = re.findall(r'(?m)^TEST-[A-Z]+-\d+\b', test_text)
        lines.append('PASS acceptance test IDs counted: %d' % len(tests))
        if len(tests) < 5:
            failures.append('Acceptance test plan has too few TEST IDs')
    except Exception as exc:
        msg = 'FAIL acceptance test plan read failed: %r' % exc
        lines.append(msg); failures.append(msg)

    lines.append('')
    if failures:
        lines.append('SUMMARY: FAIL')
        for f in failures:
            lines.append('ERROR: %s' % f)
    else:
        lines.append('SUMMARY: PASS')

    report = '\n'.join(lines) + '\n'
    REPORT_PATH.write_text(report, encoding='utf-8')
    print(report)
    return 1 if failures else 0

if __name__ == '__main__':
    sys.exit(main())
