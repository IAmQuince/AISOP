#!/usr/bin/env python
from __future__ import print_function
import sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'reports' / 'repo_health_audit_report.txt'
REQUIRED_FILES = [
    'README.md','README_START_HERE.md','CONTRIBUTING.md','SECURITY.md','SAFETY.md','SUPPORT.md',
    'CODE_OF_CONDUCT.md','NOTICE.md','LICENSE_DECISION_REQUIRED.md','CITATION.cff',
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
    ('LICENSE_DECISION_REQUIRED.md','not licensed for public reuse'),
]

def read(path): return path.read_text(encoding='utf-8')
def main():
    errors=[]; lines=[]
    REPORT.parent.mkdir(exist_ok=True)
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
    lines += ['','SUMMARY','-'*72,'SUMMARY: %s' % ('FAIL' if errors else 'PASS')]
    for e in errors: lines.append('ERROR: %s' % e)
    text='\n'.join(lines)+'\n'; REPORT.write_text(text, encoding='utf-8'); print(text)
    return 1 if errors else 0
if __name__ == '__main__': sys.exit(main())
