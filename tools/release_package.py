#!/usr/bin/env python
"""Build the full release zip: dist/<package_id>.zip unpacking to <package_id>/.

The root folder name comes from `package_id` in config/package_metadata.json,
never from the clone folder name (REQ-REL-002). A clone named `AISOP` and a
zip-extracted folder named after the package_id produce the same archive.
"""
from __future__ import print_function

import argparse
import sys
import time
from pathlib import Path

from _aisop_common import ROOT, iter_package_files, load_config, rel_posix, write_zip, zip_roots

DIST = ROOT / 'dist'
REPORT = ROOT / 'reports' / 'release_dry_run_report.txt'


def collect_members(root_name):
    return [('%s/%s' % (root_name, rel_posix(p)), p.read_bytes()) for p in iter_package_files()]


def build(dry_run=False, name=None, out_dir=None):
    cfg = load_config()
    root_name = name or cfg['package_id']
    out_dir = Path(out_dir) if out_dir else DIST
    zip_path = out_dir / (root_name + '.zip')
    files = list(iter_package_files())
    lines = ['RELEASE PACKAGE REPORT', '=' * 72,
             'timestamp: %s' % time.strftime('%Y-%m-%d %H:%M:%S'),
             'package_root: %s' % ROOT,
             'package_id: %s' % cfg['package_id'],
             'archive: %s' % zip_path,
             'internal_root: %s/' % root_name,
             'dry_run: %s' % dry_run,
             'file_count: %d' % len(files), '']
    errors, warnings = [], []
    if ROOT.name != root_name:
        warnings.append('working-copy folder %r differs from the release root %r; the archive uses %r '
                        '(clone folder names are a working-copy convention, the package_id is the '
                        'handoff identity)' % (ROOT.name, root_name, root_name))
    if not dry_run:
        write_zip(zip_path, collect_members(root_name), cfg.get('last_updated', '1980-01-01'))
        roots = zip_roots(zip_path)
        if roots != [root_name]:
            errors.append('archive internal root mismatch: %r' % roots)
        else:
            lines.append('PASS archive internal root matches basename: %s' % zip_path.name)
    else:
        lines.append('PASS dry run file discovery completed')
        lines.append('PASS archive basename would be %s.zip with internal root %s/' % (root_name, root_name))
    lines += ['', 'SUMMARY', '-' * 72, 'SUMMARY: %s' % ('FAIL' if errors else 'PASS')]
    lines += ['WARNING: %s' % w for w in warnings]
    lines += ['ERROR: %s' % e for e in errors]
    text = '\n'.join(lines) + '\n'
    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text(text, encoding='utf-8')
    print(text)
    return (1 if errors else 0), zip_path


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    ap.add_argument('--dry-run', action='store_true', help='list and name only; write no archive')
    ap.add_argument('--name', help='override the root folder and zip basename (default: package_id)')
    ap.add_argument('--out', help='output directory (default: dist/)')
    args = ap.parse_args(argv)
    code, _ = build(args.dry_run, args.name, args.out)
    return code


if __name__ == '__main__':
    sys.exit(main())
