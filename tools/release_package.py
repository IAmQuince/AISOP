#!/usr/bin/env python
from __future__ import print_function
import argparse, sys, time, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DIST=ROOT/'dist'
REPORT=ROOT/'reports'/'release_dry_run_report.txt'
EXCLUDE_DIRS={'.git','dist','__pycache__','.pytest_cache','.mypy_cache','.ruff_cache'}
def include(p):
    rel=p.relative_to(ROOT)
    if any(part in EXCLUDE_DIRS for part in rel.parts): return False
    return p.is_file()
def build(dry_run=False):
    name=ROOT.name
    zip_path=DIST/(name+'.zip')
    files=[p for p in sorted(ROOT.rglob('*')) if include(p)]
    lines=['RELEASE PACKAGE REPORT','='*72,'timestamp: %s' % time.strftime('%Y-%m-%d %H:%M:%S'),'package_root: %s' % ROOT,'archive: %s' % zip_path,'dry_run: %s' % dry_run,'file_count: %d' % len(files),'']
    errors=[]
    if name != '20260516_00_seed':
        errors.append('package root name is unexpected: %s' % name)
    if not dry_run:
        DIST.mkdir(exist_ok=True)
        if zip_path.exists(): zip_path.unlink()
        with zipfile.ZipFile(str(zip_path),'w',compression=zipfile.ZIP_DEFLATED) as z:
            for p in files:
                z.write(str(p), arcname=str(Path(name)/p.relative_to(ROOT)))
        with zipfile.ZipFile(str(zip_path),'r') as z:
            roots=sorted({n.split('/')[0] for n in z.namelist() if '/' in n})
        if roots != [name]: errors.append('archive internal root mismatch: %r' % roots)
        else: lines.append('PASS archive internal root matches basename')
    else:
        lines.append('PASS dry run file discovery completed')
        lines.append('PASS archive basename would be %s.zip with internal root %s/' % (name,name))
    lines += ['','SUMMARY','-'*72,'SUMMARY: %s' % ('FAIL' if errors else 'PASS')]
    for e in errors: lines.append('ERROR: %s' % e)
    REPORT.parent.mkdir(exist_ok=True); text='\n'.join(lines)+'\n'; REPORT.write_text(text, encoding='utf-8'); print(text)
    return (1 if errors else 0), zip_path

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--dry-run',action='store_true'); args=ap.parse_args()
    code,_=build(args.dry_run); return code
if __name__=='__main__': sys.exit(main())
