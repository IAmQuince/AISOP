#!/usr/bin/env python
"""Run every package audit in order and write reports/run_all_audits_report.txt.

    python tools/run_all_audits.py           full output
    python tools/run_all_audits.py --quiet   one line per command plus the SUMMARY block

Commands run with the current interpreter (sys.executable), so a `python3`-only
machine works. The manifest check runs last because it hashes generated files.
"""
from __future__ import print_function

import argparse
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'reports' / 'run_all_audits_report.txt'
COMMANDS = [
    ['tools/package_structure_audit.py'],
    ['tools/repo_health_audit.py'],
    ['tools/edition_audit.py'],
    ['tools/build_editions.py', '--check'],
    ['tests/smoke_test.py'],
    ['tools/requirements_trace_audit.py'],
    ['tools/secret_scan_lite.py'],
    ['tools/release_package.py', '--dry-run'],
    ['tools/manifest_update.py', '--check'],
]


def run(cmd):
    proc = subprocess.run([sys.executable] + cmd, cwd=str(ROOT), stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, universal_newlines=True)
    return proc.returncode, proc.stdout.rstrip()


def main(argv=None):
    ap = argparse.ArgumentParser(description='Run all AISOP audits')
    ap.add_argument('--quiet', action='store_true', help='print only the per-command results and SUMMARY')
    args = ap.parse_args(argv)
    lines = ['RUN ALL AUDITS REPORT', '=' * 72,
             'timestamp: %s' % time.strftime('%Y-%m-%d %H:%M:%S'),
             'package_root: %s' % ROOT, 'python: %s' % sys.version.split()[0], '']
    results, failures = [], []
    for cmd in COMMANDS:
        label = 'python ' + ' '.join(cmd)
        code, output = run(cmd)
        lines += ['COMMAND: %s' % label, output, 'RETURN_CODE: %s' % code, '-' * 72]
        results.append('%s %s' % ('PASS' if code == 0 else 'FAIL', label))
        if code:
            failures.append(label)
    summary = ['', 'RESULTS', '-' * 72] + results + ['', 'SUMMARY: %s' % ('FAIL' if failures else 'PASS')]
    summary += ['FAILED: %s' % f for f in failures]
    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text('\n'.join(lines + summary) + '\n', encoding='utf-8')
    print('\n'.join((summary[1:] if args.quiet else lines + summary)))
    if args.quiet:
        print('Full report: reports/run_all_audits_report.txt')
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
