#!/usr/bin/env python
from __future__ import print_function
import subprocess, sys, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'reports'/'run_all_audits_report.txt'
COMMANDS=[
    ['python','tools/package_structure_audit.py'],
    ['python','tools/repo_health_audit.py'],
    ['python','tests/smoke_test.py'],
    ['python','tools/requirements_trace_audit.py'],
    ['python','tools/secret_scan_lite.py'],
    ['python','tools/release_package.py','--dry-run'],
]
def main():
    lines=['RUN ALL AUDITS REPORT','='*72,'timestamp: %s' % time.strftime('%Y-%m-%d %H:%M:%S'),'package_root: %s' % ROOT,'']
    failures=[]
    for cmd in COMMANDS:
        lines.append('COMMAND: %s' % ' '.join(cmd))
        proc=subprocess.run(cmd,cwd=str(ROOT),stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        lines.append(proc.stdout.rstrip())
        lines.append('RETURN_CODE: %s' % proc.returncode)
        lines.append('-'*72)
        if proc.returncode: failures.append(' '.join(cmd))
    lines.append('SUMMARY: %s' % ('FAIL' if failures else 'PASS'))
    for f in failures: lines.append('FAILED: %s' % f)
    REPORT.parent.mkdir(exist_ok=True); text='\n'.join(lines)+'\n'; REPORT.write_text(text, encoding='utf-8'); print(text)
    return 1 if failures else 0
if __name__=='__main__': sys.exit(main())
