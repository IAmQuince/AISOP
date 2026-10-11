#!/usr/bin/env python
"""AISOP lite audit for your own package (one file, standard library, Python 2.7 or 3).

    python aisop_check.py                   check the current folder
    python aisop_check.py --root PATH       check a package folder or a .zip
    python aisop_check.py --root PATH --run also run the script's --smoke-test
    python aisop_check.py --explain         print the checks, for checking by hand

Copy this file into your package's tools/ folder. The CHECKS table below is
also published as templates/MANUAL_AUDIT_CHECKLIST.md, so the by-hand path and
this script cannot drift apart.
"""
from __future__ import print_function

import io
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

INTAKE = ['README_START_HERE.md', 'CHANGELOG.md', 'FEATURE_INVENTORY.md',
          'ACCEPTANCE_TEST_PLAN.md', 'KNOWN_LIMITATIONS.md']
HEADER_KEYS = ['document_id', 'title', 'version', 'revision', 'status',
               'last_updated', 'package_id', 'machine_reference_prefix', 'normative_status']
FLAGS = ['--version', '--smoke-test', '--diagnostics']
NAME_RULE = re.compile(r'^\d{8}_\d{2}_[a-z0-9][a-z0-9_-]*$')
LINK = re.compile(r'\[[^\]\n]*\]\(([^)\s]+)\)')

CHECKS = [
    ('CHECK-01', 'Intake documents',
     'The root holds README_START_HERE.md, CHANGELOG.md, FEATURE_INVENTORY.md, ACCEPTANCE_TEST_PLAN.md and KNOWN_LIMITATIONS.md, none empty.'),
    ('CHECK-02', 'Document-control headers',
     'Each intake document starts with a --- header holding: ' + ', '.join(HEADER_KEYS) + '.'),
    ('CHECK-03', 'One package identity',
     'Every header has the same package_id, written yyyymmdd_00_short-description.'),
    ('CHECK-04', 'Folder and zip names',
     'A zip holds exactly one top folder named like the zip; a dated folder name equals the package_id.'),
    ('CHECK-05', 'Runnable script with diagnostics',
     'A .py file in the root offers --version, --smoke-test and --diagnostics.'),
    ('CHECK-06', 'Feature and test IDs',
     'FEATURE_INVENTORY.md lists FEAT- IDs; ACCEPTANCE_TEST_PLAN.md lists TEST- IDs; every TEST- ID named in the inventory exists in the plan.'),
    ('CHECK-07', 'Dated changelog',
     'CHANGELOG.md has at least one entry with a yyyy-mm-dd date.'),
    ('CHECK-08', 'Links resolve',
     'Every relative link in the Markdown files points at a file that exists.'),
]


def read(path):
    with io.open(path, encoding='utf-8') as handle:
        return handle.read()


def header(text):
    if not text.startswith('---\n'):
        return {}
    end = text.find('\n---\n', 4)
    if end == -1:
        return {}
    result = {}
    for line in text[4:end].splitlines():
        if ':' in line and not line.startswith((' ', '#')):
            key, value = line.split(':', 1)
            result[key.strip()] = value.strip().strip('"')
    return result


def markdown_files(root):
    for base, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        for name in files:
            if name.endswith('.md'):
                yield os.path.join(base, name)


def check_intake(root, zip_name):
    missing = [n for n in INTAKE if not os.path.isfile(os.path.join(root, n))
               or os.path.getsize(os.path.join(root, n)) == 0]
    return not missing, 'missing or empty: %s' % ', '.join(missing) if missing else 'all five present'


def check_headers(root, zip_name):
    bad = []
    for name in INTAKE:
        path = os.path.join(root, name)
        if os.path.isfile(path):
            keys = header(read(path))
            lost = [k for k in HEADER_KEYS if not keys.get(k)]
            if lost:
                bad.append('%s lacks %s' % (name, ', '.join(lost)))
    return not bad, '; '.join(bad) or 'complete'


def package_ids(root):
    return set(header(read(p)).get('package_id', '') for p in markdown_files(root))


def check_identity(root, zip_name):
    ids = package_ids(root) - set([''])
    if len(ids) != 1:
        return False, 'package_id values found: %s' % (sorted(ids) or 'none')
    pid = ids.pop()
    return bool(NAME_RULE.match(pid)), 'package_id %s %s the naming rule' % (
        pid, 'follows' if NAME_RULE.match(pid) else 'breaks')


def check_names(root, zip_name):
    ids = sorted(package_ids(root) - set(['']))
    folder = os.path.basename(os.path.abspath(root))
    if zip_name:
        stem = os.path.splitext(os.path.basename(zip_name))[0]
        if folder != stem:
            return False, 'zip %s holds folder %s' % (os.path.basename(zip_name), folder)
    if re.match(r'^\d{8}_\d{2}_', folder):
        allowed = [p for p in ids if folder == p or folder.startswith(p + '_')]
        return bool(allowed), 'folder %s, package_id %s' % (folder, ids)
    return True, 'folder %s is not dated; only the zip rule applies' % folder


def check_script(root, zip_name):
    for name in sorted(os.listdir(root)):
        if name.endswith('.py') and name != 'aisop_check.py':
            text = read(os.path.join(root, name))
            if all(flag in text for flag in FLAGS):
                return True, name
    return False, 'no root .py file offers %s' % ', '.join(FLAGS)


def check_ids(root, zip_name):
    inv = os.path.join(root, 'FEATURE_INVENTORY.md')
    plan = os.path.join(root, 'ACCEPTANCE_TEST_PLAN.md')
    if not (os.path.isfile(inv) and os.path.isfile(plan)):
        return False, 'inventory or test plan missing'
    feats = re.findall(r'\bFEAT-\d+\b', read(inv))
    planned = set(re.findall(r'\bTEST-[A-Z]+-\d+\b', read(plan)))
    unknown = sorted(set(re.findall(r'\bTEST-[A-Z]+-\d+\b', read(inv))) - planned)
    ok = bool(feats) and bool(planned) and not unknown
    return ok, '%d FEAT, %d TEST%s' % (len(set(feats)), len(planned),
                                       ', unknown: %s' % ', '.join(unknown) if unknown else '')


def check_changelog(root, zip_name):
    path = os.path.join(root, 'CHANGELOG.md')
    dated = os.path.isfile(path) and re.search(r'\b\d{4}-\d{2}-\d{2}\b', read(path))
    return bool(dated), 'dated entry found' if dated else 'no yyyy-mm-dd entry'


def check_links(root, zip_name):
    broken = []
    for path in markdown_files(root):
        for target in LINK.findall(read(path)):
            if re.match(r'^[a-z]+:', target) or target.startswith('#'):
                continue
            target = target.split('#')[0]
            if target and not os.path.exists(os.path.join(os.path.dirname(path), target)):
                broken.append('%s -> %s' % (os.path.relpath(path, root), target))
    return not broken, '; '.join(broken) or 'all resolve'


FUNCTIONS = [check_intake, check_headers, check_identity, check_names,
             check_script, check_ids, check_changelog, check_links]


def run_smoke(root):
    ok, name = check_script(root, None)
    if not ok:
        return False, name
    proc = subprocess.Popen([sys.executable, name, '--smoke-test'], cwd=root,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = proc.communicate()[0].decode('utf-8', 'replace').strip().splitlines()
    last = output[-1] if output else 'no output'
    return proc.returncode == 0, '%s --smoke-test exit %d (%s)' % (name, proc.returncode, last)


def audit(root, zip_name=None, run=False):
    print('AISOP CHECK REPORT')
    print('root: %s' % root)
    failures = 0
    for (check_id, title, _), func in zip(CHECKS, FUNCTIONS):
        ok, detail = func(root, zip_name)
        failures += 0 if ok else 1
        print('%s %s %s: %s' % ('PASS' if ok else 'FAIL', check_id, title, detail))
    if run:
        ok, detail = run_smoke(root)
        failures += 0 if ok else 1
        print('%s RUN smoke test: %s' % ('PASS' if ok else 'FAIL', detail))
    print('SUMMARY: %s' % ('FAIL' if failures else 'PASS'))
    return 1 if failures else 0


def explain():
    for check_id, title, manual in CHECKS:
        print('%s %s\n    %s' % (check_id, title, manual))
    return 0


def main(argv):
    args = list(argv)
    if '--explain' in args:
        return explain()
    root = args[args.index('--root') + 1] if '--root' in args else '.'
    run = '--run' in args
    if root.endswith('.zip'):
        tmp = tempfile.mkdtemp(prefix='aisop_check_')
        try:
            with zipfile.ZipFile(root) as archive:
                archive.extractall(tmp)
            tops = [n for n in os.listdir(tmp) if not n.startswith('.')]
            if len(tops) != 1:
                print('FAIL CHECK-04 Folder and zip names: zip holds %d top-level entries' % len(tops))
                print('SUMMARY: FAIL')
                return 1
            return audit(os.path.join(tmp, tops[0]), zip_name=root, run=run)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    return audit(root, run=run)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
