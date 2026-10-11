#!/usr/bin/env python
from __future__ import print_function
import json, re, subprocess, sys, time
from pathlib import Path
from _aisop_common import iter_package_files
ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'reports' / 'repo_health_audit_report.txt'
CONFIG = ROOT / 'config' / 'package_metadata.json'
def read(path): return path.read_text(encoding='utf-8')

def load_config():
    return json.loads(read(CONFIG))

def _indent(line):
    return len(line) - len(line.lstrip())

def push_branches(workflow_text):
    """Return on.push.branches (inline `[a, b]` or dash-list form) without a YAML parser."""
    lines = workflow_text.splitlines()
    for i, line in enumerate(lines):
        if not re.match(r'^\s*push:\s*$', line):
            continue
        block = []
        for follow in lines[i + 1:]:
            if follow.strip() and _indent(follow) <= _indent(line):
                break
            block.append(follow)
        for j, entry in enumerate(block):
            m = re.match(r'^\s*branches:\s*(.*)$', entry)
            if not m:
                continue
            inline = m.group(1).strip()
            if inline.startswith('['):
                return [b.strip().strip('\'"') for b in inline.strip('[]').split(',') if b.strip()]
            items = []
            for item in block[j + 1:]:
                d = re.match(r'^\s*-\s*(\S+)\s*$', item)
                if not d:
                    break
                items.append(d.group(1).strip('\'"'))
            return items
    return []

def check_license(cfg, errors, lines):
    """TEST-LIC-001: the configured license file exists, names its license, and NOTICE.md agrees."""
    lic_file = cfg.get('license_file', '')
    lic_name = cfg.get('license_name', '')
    lic = ROOT / lic_file if lic_file else None
    notice = ROOT / 'NOTICE.md'
    checks = [
        (bool(lic_file and lic_name), 'config names license_file and license_name'),
        (bool(lic and lic.is_file() and lic_name in read(lic)), '%s contains %r' % (lic_file, lic_name)),
        (notice.is_file() and lic_name in read(notice) and lic_file in read(notice),
         'NOTICE.md names %r and %s' % (lic_name, lic_file)),
    ]
    for ok, label in checks:
        if ok: lines.append('PASS %s' % label)
        else:
            msg = 'FAIL %s (TEST-LIC-001)' % label; lines.append(msg); errors.append(msg)

def check_ci_branch(cfg, errors, lines):
    """TEST-CI-002: ci.yml runs on push to the configured default branch."""
    branch = cfg.get('default_branch', '')
    ci = ROOT / '.github' / 'workflows' / 'ci.yml'
    branches = push_branches(read(ci)) if ci.is_file() else []
    if branch and branch in branches:
        lines.append('PASS ci.yml on.push.branches %s contains default_branch %r' % (branches, branch))
    else:
        msg = 'FAIL ci.yml on.push.branches %s does not contain default_branch %r (TEST-CI-002)' % (branches, branch)
        lines.append(msg); errors.append(msg)

def tracked_runtime_reports():
    """Return tracked reports/*.txt (top level only) or None when git is unavailable."""
    if not (ROOT / '.git').exists():
        return None
    try:
        out = subprocess.run(['git', 'ls-files', 'reports'], cwd=str(ROOT), stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, universal_newlines=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return None
    return [f for f in out.splitlines() if re.match(r'^reports/[^/]+\.txt$', f)]

def check_runtime_reports(errors, lines):
    """TEST-RPT-001: runtime reports are git-ignored and not tracked; baselines stay committed."""
    ignore = read(ROOT / '.gitignore') if (ROOT / '.gitignore').exists() else ''
    if 'reports/*.txt' in ignore.splitlines():
        lines.append('PASS .gitignore ignores reports/*.txt')
    else:
        msg = 'FAIL .gitignore does not ignore reports/*.txt (TEST-RPT-001)'; lines.append(msg); errors.append(msg)
    tracked = tracked_runtime_reports()
    if tracked is None:
        lines.append('SKIP git unavailable or not a clone; tracked-report check not applicable')
    elif tracked:
        msg = 'FAIL runtime reports are tracked: %s (TEST-RPT-001)' % ', '.join(tracked); lines.append(msg); errors.append(msg)
    else:
        lines.append('PASS no runtime reports/*.txt are tracked')

REPORT_TITLE = re.compile(r'(?i)package report')
REPORT_EXEMPT = {'CHANGELOG.md', 'WORKPLAN_CURRENT_RUN.md', 'docs/300_AISOP_EXPANSION_GAMEPLAN_REV003.md'}

def _is_title(line):
    """A Markdown heading, a short numbered title (not a sentence), or a field label ending in ':'."""
    s = line.strip()
    numbered_title = bool(re.match(r'^\d+\.\s', s)) and len(s) <= 60 and not s.endswith('.')
    return s.startswith('#') or numbered_title or s.endswith(':')

def check_canonical_report(cfg, errors, lines):
    """TEST-RPT-002: delivery SOPs cite the one report template; no competing report-format title."""
    template = cfg.get('report_template', '')
    if template and (ROOT / template).is_file():
        lines.append('PASS canonical report template exists: %s' % template)
    else:
        msg = 'FAIL canonical report template missing: %r (TEST-RPT-002)' % template; lines.append(msg); errors.append(msg)
        return
    for rel in cfg.get('report_template_citers', []):
        path = ROOT / rel
        if path.is_file() and template in read(path):
            lines.append('PASS %s cites %s' % (rel, template))
        else:
            msg = 'FAIL %s does not cite %s (TEST-RPT-002)' % (rel, template); lines.append(msg); errors.append(msg)
    canonical = cfg.get('report_canonical_source', '')
    for path in iter_package_files():
        rel = path.relative_to(ROOT).as_posix()
        if path.suffix != '.md' or rel in REPORT_EXEMPT or rel == template:
            continue
        doc_lines = read(path).splitlines()
        for i, line in enumerate(doc_lines):
            if not (REPORT_TITLE.search(line) and _is_title(line)):
                continue
            window = '\n'.join(doc_lines[i:i + 4])
            if rel != canonical and template not in window:
                msg = 'FAIL %s:%d defines a package-report format without citing %s (TEST-RPT-002)' % (rel, i + 1, template)
                lines.append(msg); errors.append(msg)


def check_release_workflow(errors, lines):
    """TEST-REL-003: release assets are built only after a green audit run of the tagged commit."""
    path = ROOT / '.github' / 'workflows' / 'release.yml'
    text = read(path) if path.is_file() else ''
    audit_at, build_at = text.find('tools/run_all_audits.py'), text.find('tools/build_editions.py zips')
    checks = [
        (bool(re.search(r"tags:\s*\[\s*'v\*'\s*\]", text)), 'release.yml runs on v* tags'),
        (0 <= audit_at < build_at, 'release.yml runs run_all_audits.py before build_editions.py zips'),
        ('GITHUB_REF_NAME' in text and "'v' + v" in text, 'release.yml checks the tag against the configured version'),
    ]
    for ok, label in checks:
        if ok: lines.append('PASS %s' % label)
        else:
            msg = 'FAIL %s (TEST-REL-003)' % label; lines.append(msg); errors.append(msg)

def main():
    errors=[]; lines=[]
    REPORT.parent.mkdir(exist_ok=True)
    cfg = load_config()
    lines += ['REPO HEALTH AUDIT REPORT','='*72,'timestamp: %s' % time.strftime('%Y-%m-%d %H:%M:%S'),'package_root: %s' % ROOT,'']
    lines += ['REQUIRED REPOSITORY FILES','-'*72]
    for rel in cfg.get('required_repository_files', []):
        p=ROOT/rel
        if p.exists() and p.stat().st_size>0: lines.append('PASS %s' % rel)
        else:
            msg='FAIL missing or empty: %s' % rel; lines.append(msg); errors.append(msg)
    lines += ['','CONTENT CHECKS','-'*72]
    for rel, needle in cfg.get('content_checks', []):
        p=ROOT/rel
        if p.exists() and needle in read(p): lines.append('PASS %s contains %r' % (rel, needle))
        else:
            msg='FAIL %s missing content %r' % (rel, needle); lines.append(msg); errors.append(msg)
    lines += ['','LICENSE','-'*72]
    check_license(cfg, errors, lines)
    lines += ['','CI DEFAULT BRANCH','-'*72]
    check_ci_branch(cfg, errors, lines)
    lines += ['','CANONICAL FINAL PACKAGE REPORT','-'*72]
    check_canonical_report(cfg, errors, lines)
    lines += ['','RELEASE WORKFLOW','-'*72]
    check_release_workflow(errors, lines)
    lines += ['','RUNTIME REPORTS','-'*72]
    check_runtime_reports(errors, lines)
    lines += ['','SUMMARY','-'*72,'SUMMARY: %s' % ('FAIL' if errors else 'PASS')]
    for e in errors: lines.append('ERROR: %s' % e)
    text='\n'.join(lines)+'\n'; REPORT.write_text(text, encoding='utf-8'); print(text)
    return 1 if errors else 0
if __name__ == '__main__': sys.exit(main())
