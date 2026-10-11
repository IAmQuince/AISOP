#!/usr/bin/env python
from __future__ import print_function
import json, re, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'reports' / 'repo_health_audit_report.txt'
CONFIG = ROOT / 'config' / 'package_metadata.json'
REQUIRED_FILES = [
    'README.md','README_START_HERE.md','CONTRIBUTING.md','SECURITY.md','SAFETY.md','SUPPORT.md',
    'CODE_OF_CONDUCT.md','NOTICE.md','CITATION.cff',
    '.gitignore','.gitattributes','.editorconfig',
    '.github/PULL_REQUEST_TEMPLATE.md','.github/dependabot.yml',
    '.github/workflows/ci.yml','.github/workflows/package_audit.yml','.github/workflows/release_dry_run.yml',
    '.github/ISSUE_TEMPLATE/bug_report.yml','.github/ISSUE_TEMPLATE/feature_request.yml',
    '.github/ISSUE_TEMPLATE/documentation_update.yml','.github/ISSUE_TEMPLATE/safety_or_security_review.yml',
    '.github/ISSUE_TEMPLATE/package_regression.yml',
    'docs/080_AISOP_AS_A_SPACE_OF_PRACTICES.md','docs/090_GITHUB_REPOSITORY_BOOTSTRAP_SOP.md',
    'docs/100_RELEASE_VERSIONING_AND_ZIP_HANDOFF_SOP.md','docs/110_SECURITY_AND_SAFETY_BASELINE_SOP.md',
    'docs/120_CONTRIBUTION_REVIEW_AND_ISSUE_WORKFLOW_SOP.md','docs/130_PRODUCT_LAUNCH_READINESS_CHECKLIST.md',
    'docs/140_LICENSE_IP_AND_ATTRIBUTION_DECISION_GUIDE.md','docs/150_CI_TESTING_AND_REPO_HEALTH_AUDIT_GUIDE.md',
    'docs/160_MAINTAINER_PLAYBOOK.md','docs/165_AI_AGENT_HANDOFF_PROTOCOL.md'
]
CONTENT_CHECKS = [
    ('README.md','README_START_HERE.md'),
    ('README.md','space of practices'),
    ('README.md','GitHub'),
    ('docs/080_AISOP_AS_A_SPACE_OF_PRACTICES.md','practice space'),
    ('docs/090_GITHUB_REPOSITORY_BOOTSTRAP_SOP.md','zip package'),
    ('.github/workflows/ci.yml','run_all_audits.py'),
    ('SECURITY.md','No-secrets'),
    ('SAFETY.md','SAFE-CLASS-3'),
]

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

def main():
    errors=[]; lines=[]
    REPORT.parent.mkdir(exist_ok=True)
    cfg = load_config()
    lines += ['REPO HEALTH AUDIT REPORT','='*72,'timestamp: %s' % time.strftime('%Y-%m-%d %H:%M:%S'),'package_root: %s' % ROOT,'']
    lines += ['REQUIRED REPOSITORY FILES','-'*72]
    for rel in REQUIRED_FILES:
        p=ROOT/rel
        if p.exists() and p.stat().st_size>0: lines.append('PASS %s' % rel)
        else:
            msg='FAIL missing or empty: %s' % rel; lines.append(msg); errors.append(msg)
    lines += ['','CONTENT CHECKS','-'*72]
    for rel, needle in CONTENT_CHECKS:
        p=ROOT/rel
        if p.exists() and needle in read(p): lines.append('PASS %s contains %r' % (rel, needle))
        else:
            msg='FAIL %s missing content %r' % (rel, needle); lines.append(msg); errors.append(msg)
    lines += ['','LICENSE','-'*72]
    check_license(cfg, errors, lines)
    lines += ['','CI DEFAULT BRANCH','-'*72]
    check_ci_branch(cfg, errors, lines)
    lines += ['','SUMMARY','-'*72,'SUMMARY: %s' % ('FAIL' if errors else 'PASS')]
    for e in errors: lines.append('ERROR: %s' % e)
    text='\n'.join(lines)+'\n'; REPORT.write_text(text, encoding='utf-8'); print(text)
    return 1 if errors else 0
if __name__ == '__main__': sys.exit(main())
