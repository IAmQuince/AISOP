#!/usr/bin/env python
"""Move the package to a new identity: rewrite `package_id` and `version` everywhere they are recorded.

    python tools/bump_release.py --package-id 20261011_00_aisop --version 0.3.0
    python tools/bump_release.py --check      exit 1 if any header disagrees with config

Updates config/package_metadata.json, requirements/requirements_catalog.json,
CITATION.cff, and the `package_id` and `version` lines of every document
header (registered example packages keep their own identity). It never
touches `revision` or `last_updated`, so the commit shows the identity change
and nothing else (docs/300 RISK-007). Run `python tools/build_editions.py all`
and the audits afterwards.
"""
from __future__ import print_function

import argparse
import json
import re
import sys

from _aisop_common import CONFIG_PATH, ROOT, iter_package_files, load_config, read_text, rel_posix

CATALOG = ROOT / 'requirements' / 'requirements_catalog.json'
CITATION = ROOT / 'CITATION.cff'
NAME_RULE = re.compile(r'^\d{8}_\d{2}_[a-z0-9][a-z0-9_-]*$')
VERSION_RULE = re.compile(r'^\d+\.\d+\.\d+$')


def header_targets(cfg):
    examples = tuple(r.rstrip('/') + '/' for r in cfg.get('example_packages', []))
    for path in iter_package_files():
        rel = rel_posix(path)
        if path.suffix == '.md' and not rel.startswith('.github/') and not rel.startswith(examples):
            yield path


def rewrite_header(text, package_id, version):
    """Replace package_id/version lines inside the leading front matter only."""
    if not text.startswith('---\n'):
        return text
    end = text.find('\n---\n', 4)
    if end == -1:
        return text
    head = re.sub(r'(?m)^package_id: .*$', 'package_id: %s' % package_id, text[:end])
    head = re.sub(r'(?m)^version: .*$', 'version: %s' % version, head)
    return head + text[end:]


def mismatches(cfg):
    found = []
    for path in header_targets(cfg):
        text = read_text(path)
        if rewrite_header(text, cfg['package_id'], cfg['version']) != text:
            found.append(rel_posix(path))
    return found


def bump(package_id, version):
    cfg = load_config()
    old = (cfg['package_id'], cfg['version'])
    cfg['package_id'], cfg['version'] = package_id, version
    CONFIG_PATH.write_text(json.dumps(cfg, indent=2) + '\n', encoding='utf-8')
    catalog = json.loads(read_text(CATALOG))
    catalog['package_id'], catalog['version'] = package_id, version
    CATALOG.write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    if CITATION.is_file():
        CITATION.write_text(re.sub(r'(?m)^version: .*$', 'version: "%s"' % version, read_text(CITATION)),
                            encoding='utf-8')
    changed = 0
    for path in header_targets(cfg):
        text = read_text(path)
        new = rewrite_header(text, package_id, version)
        if new != text:
            path.write_text(new, encoding='utf-8')
            changed += 1
    print('identity %s %s -> %s %s; %d headers rewritten' % (old[0], old[1], package_id, version, changed))
    print('next: python tools/build_editions.py all && python tools/run_all_audits.py')
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description='Rewrite package_id and version from one place')
    ap.add_argument('--package-id', help='new package_id, yyyymmdd_00_short-description')
    ap.add_argument('--version', help='new version, MAJOR.MINOR.PATCH')
    ap.add_argument('--check', action='store_true', help='report headers that disagree with config')
    args = ap.parse_args(argv)
    if args.check:
        bad = mismatches(load_config())
        for rel in bad:
            print('FAIL header package_id/version differs from config: %s' % rel)
        print('SUMMARY: %s' % ('FAIL' if bad else 'PASS'))
        return 1 if bad else 0
    if not (args.package_id and args.version):
        ap.error('give --package-id and --version, or --check')
    if not NAME_RULE.match(args.package_id) or not VERSION_RULE.match(args.version):
        ap.error('package_id must look like 20261011_00_aisop and version like 0.3.0')
    return bump(args.package_id, args.version)


if __name__ == '__main__':
    sys.exit(main())
