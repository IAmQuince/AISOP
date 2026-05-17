#!/usr/bin/env python
from __future__ import print_function
import sys, zipfile, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'reports' / 'archive_name_audit_report.txt'

def audit_zip(zip_path):
    z=Path(zip_path)
    errors=[]; lines=[]
    lines += ['ARCHIVE NAME AUDIT REPORT','='*72,'timestamp: %s' % time.strftime('%Y-%m-%d %H:%M:%S'),'archive: %s' % z,'']
    if not z.exists():
        errors.append('archive does not exist')
    else:
        with zipfile.ZipFile(str(z),'r') as zh:
            roots=sorted({name.split('/')[0] for name in zh.namelist() if name and '/' in name})
        expected=z.stem
        lines.append('expected_root: %s' % expected)
        lines.append('roots_found: %s' % roots)
        if roots == [expected]: lines.append('PASS archive basename matches single internal root folder')
        else: errors.append('archive basename/internal root mismatch')
    lines += ['','SUMMARY','-'*72,'SUMMARY: %s' % ('FAIL' if errors else 'PASS')]
    for e in errors: lines.append('ERROR: %s' % e)
    text='\n'.join(lines)+'\n'; REPORT.parent.mkdir(exist_ok=True); REPORT.write_text(text, encoding='utf-8'); print(text)
    return 1 if errors else 0
if __name__ == '__main__':
    if len(sys.argv)<2:
        print('usage: python tools/archive_name_audit.py path/to/archive.zip')
        sys.exit(2)
    sys.exit(audit_zip(sys.argv[1]))
