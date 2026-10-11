#!/usr/bin/env python
"""AISOP package smoke test.

Positive checks on the controlled documents plus scripted end-to-end cases
that run the real tools on a copy of the tree in a temporary directory, so
the gates are re-run every time instead of being trusted from a past log.
"""
from __future__ import print_function

import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE_ROOT / 'tools'))

from _aisop_common import iter_package_files, load_config, read_text, rel_posix, zip_roots  # noqa: E402

REPORT_PATH = PACKAGE_ROOT / 'reports' / 'smoke_test_report.txt'


class Report(object):
    def __init__(self):
        self.lines = []
        self.failures = []

    def check(self, ok, label):
        self.lines.append('%s %s' % ('PASS' if ok else 'FAIL', label))
        if not ok:
            self.failures.append(label)
        return ok

    def section(self, title):
        self.lines += ['', title, '-' * 72]


# ---------------------------------------------------------------------------
# Helpers for scripted cases
# ---------------------------------------------------------------------------

def copy_package(dest):
    """Copy the package files (git-ignore-aware) into dest and return dest."""
    dest = Path(dest)
    for path in iter_package_files(PACKAGE_ROOT):
        target = dest / rel_posix(path, PACKAGE_ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(str(path), str(target))
    return dest


def run_tool(root, *args):
    proc = subprocess.run([sys.executable] + list(args), cwd=str(root), stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, universal_newlines=True)
    return proc.returncode, proc.stdout


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def check_required_documents(rep):
    rep.section('REQUIRED DOCUMENTS')
    for rel in ['README_START_HERE.md', 'docs/005_PRODUCT_REQUIREMENTS.md', 'FEATURE_INVENTORY.md',
                'ACCEPTANCE_TEST_PLAN.md', 'requirements/requirements_catalog.json']:
        path = PACKAGE_ROOT / rel
        rep.check(path.exists() and path.stat().st_size > 0, 'exists and non-empty: %s' % rel)


def check_id_counts(rep):
    rep.section('ID COUNTS')
    try:
        reqs = json.loads(read_text(PACKAGE_ROOT / 'requirements' / 'requirements_catalog.json'))['requirements']
        rep.check(len(reqs) >= 5, 'requirement catalog loaded with %d entries' % len(reqs))
    except Exception as exc:  # report, do not crash the smoke test
        rep.check(False, 'requirement catalog loads: %r' % exc)
    feats = re.findall(r'(?m)^FEAT-\d+\b', read_text(PACKAGE_ROOT / 'FEATURE_INVENTORY.md'))
    rep.check(len(feats) >= 5, 'feature IDs counted: %d' % len(feats))
    tests = re.findall(r'(?m)^TEST-[A-Z]+-\d+\b', read_text(PACKAGE_ROOT / 'ACCEPTANCE_TEST_PLAN.md'))
    rep.check(len(tests) >= 5, 'acceptance test IDs counted: %d' % len(tests))


def check_release_root_any_folder(rep, tmp):
    """TEST-REL-002: a copy in a differently named folder releases as <package_id>/."""
    rep.section('RELEASE ROOT FROM PACKAGE_ID (TEST-REL-002)')
    pid = load_config()['package_id']
    clone = copy_package(Path(tmp) / 'Renamed_Working_Copy')
    out = Path(tmp) / 'out'
    code, output = run_tool(clone, 'tools/release_package.py', '--out', str(out))
    zip_path = out / (pid + '.zip')
    rep.check(code == 0 and zip_path.is_file(), 'release from folder %r writes %s' % (clone.name, zip_path.name))
    if zip_path.is_file():
        rep.check(zip_roots(zip_path) == [pid], 'archive internal root is %s/' % pid)
        code, _ = run_tool(clone, 'tools/archive_name_audit.py', str(zip_path))
        rep.check(code == 0, 'archive_name_audit passes on the built archive')
    rep.check('WARNING' in output and 'Renamed_Working_Copy' in output,
              'release tool warns that the working-copy folder differs from the release root')


def main():
    rep = Report()
    rep.lines += ['PACKAGE SMOKE TEST REPORT', '=' * 72,
                  'timestamp: %s' % time.strftime('%Y-%m-%d %H:%M:%S'),
                  'python: %s' % sys.version.split()[0], 'package_root: %s' % PACKAGE_ROOT]
    check_required_documents(rep)
    check_id_counts(rep)
    tmp = tempfile.mkdtemp(prefix='aisop_smoke_')
    try:
        check_release_root_any_folder(rep, tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    rep.lines += ['', 'SUMMARY: %s' % ('FAIL' if rep.failures else 'PASS')]
    rep.lines += ['ERROR: %s' % f for f in rep.failures]
    report = '\n'.join(rep.lines) + '\n'
    REPORT_PATH.parent.mkdir(exist_ok=True)
    REPORT_PATH.write_text(report, encoding='utf-8')
    print(report)
    return 1 if rep.failures else 0


if __name__ == '__main__':
    sys.exit(main())
