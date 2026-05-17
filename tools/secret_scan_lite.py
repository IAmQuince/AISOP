#!/usr/bin/env python
from __future__ import print_function
import re, sys, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'reports'/'secret_scan_lite_report.txt'
SKIP_DIRS={'.git','dist','__pycache__','.pytest_cache','.mypy_cache','.ruff_cache'}
PATTERNS=[
    ('private_key', re.compile(r'-----BEGIN (RSA |EC |OPENSSH |DSA |)?PRIVATE KEY-----')),
    ('generic_api_key_assignment', re.compile(r'(?i)\b(api[_-]?key|secret|token|password)\b\s*[:=]\s*[\"\']?[A-Za-z0-9_\-]{20,}')),
    ('github_token', re.compile(r'gh[pousr]_[A-Za-z0-9_]{20,}')),
    ('aws_access_key', re.compile(r'AKIA[0-9A-Z]{16}')),
]
TEXT_EXT={'.md','.py','.json','.yml','.yaml','.txt','.cff','.gitignore','.gitattributes','.editorconfig'}
def should_scan(p):
    if any(part in SKIP_DIRS for part in p.parts): return False
    if p.name in {'.gitignore','.gitattributes','.editorconfig'}: return True
    return p.suffix.lower() in TEXT_EXT

def main():
    hits=[]; lines=[]
    lines += ['SECRET SCAN LITE REPORT','='*72,'timestamp: %s' % time.strftime('%Y-%m-%d %H:%M:%S'),'package_root: %s' % ROOT,'']
    for p in sorted(ROOT.rglob('*')):
        if not p.is_file() or not should_scan(p): continue
        try: txt=p.read_text(encoding='utf-8', errors='ignore')
        except TypeError: txt=p.read_text()
        rel=p.relative_to(ROOT).as_posix()
        for name,pat in PATTERNS:
            for m in pat.finditer(txt):
                line=txt.count('\n',0,m.start())+1
                hits.append((rel,line,name))
    if hits:
        lines += ['POTENTIAL SECRET HITS','-'*72]
        for rel,line,name in hits: lines.append('FAIL %s:%s pattern=%s' % (rel,line,name))
    else:
        lines.append('PASS no configured secret-like patterns found')
    lines += ['','SUMMARY','-'*72,'SUMMARY: %s' % ('FAIL' if hits else 'PASS')]
    REPORT.parent.mkdir(exist_ok=True); text='\n'.join(lines)+'\n'; REPORT.write_text(text, encoding='utf-8'); print(text)
    return 1 if hits else 0
if __name__=='__main__': sys.exit(main())
