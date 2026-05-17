#!/usr/bin/env python
from __future__ import print_function
import json, re, sys, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'reports'/'requirements_trace_audit_report.txt'
def read(p): return p.read_text(encoding='utf-8')
def main():
    errors=[]; lines=[]
    req=json.loads(read(ROOT/'requirements'/'requirements_catalog.json'))
    reqs=req.get('requirements',[])
    prod=read(ROOT/'docs'/'005_PRODUCT_REQUIREMENTS.md')
    acc=read(ROOT/'ACCEPTANCE_TEST_PLAN.md')
    trace=read(ROOT/'REQUIREMENTS_TRACEABILITY_MATRIX.md')
    lines += ['REQUIREMENTS TRACE AUDIT REPORT','='*72,'timestamp: %s' % time.strftime('%Y-%m-%d %H:%M:%S'),'']
    ids=[r.get('id') for r in reqs]
    if len(ids)!=len(set(ids)): errors.append('duplicate requirement IDs')
    for r in reqs:
        rid=r.get('id',''); vid=r.get('verification','')
        if rid not in prod: errors.append('%s missing from docs/005_PRODUCT_REQUIREMENTS.md' % rid)
        if vid and vid not in acc: errors.append('%s verification %s missing from ACCEPTANCE_TEST_PLAN.md' % (rid,vid))
        if rid not in trace: errors.append('%s missing from REQUIREMENTS_TRACEABILITY_MATRIX.md' % rid)
    if errors:
        for e in errors: lines.append('FAIL '+e)
    else:
        lines.append('PASS all %d requirements have product doc, acceptance-test, and traceability references' % len(reqs))
    lines += ['','SUMMARY','-'*72,'SUMMARY: %s' % ('FAIL' if errors else 'PASS')]
    for e in errors: lines.append('ERROR: %s' % e)
    REPORT.parent.mkdir(exist_ok=True); text='\n'.join(lines)+'\n'; REPORT.write_text(text, encoding='utf-8'); print(text)
    return 1 if errors else 0
if __name__=='__main__': sys.exit(main())
