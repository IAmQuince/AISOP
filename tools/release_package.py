#!/usr/bin/env python
"""Build release archives: a thin wrapper over tools/build_editions.py.

    python tools/release_package.py                    dist/<package_id>.zip (Full edition)
    python tools/release_package.py --edition all      every release asset, then archive_name_audit on each zip
    python tools/release_package.py --dry-run          names only; writes no archive
    python tools/release_package.py --name NAME        override the Full archive's root and basename

The root folder comes from `package_id` in config/package_metadata.json,
never from the working-copy folder name (REQ-REL-002); edition archives are
named `<package_id>_<edition>` (docs/166_EDITIONS_AND_TIERS_SOP.md).
"""
from __future__ import print_function

import argparse
import subprocess
import sys
import time
from pathlib import Path

from _aisop_common import ROOT, write_zip, zip_roots
from _aisop_editions import Tree, config_for, root_folder
from build_editions import cmd_zips, stage_edition

DIST = ROOT / 'dist'
REPORT = ROOT / 'reports' / 'release_dry_run_report.txt'


def archive_name_audit(zip_path):
    proc = subprocess.run([sys.executable, str(ROOT / 'tools' / 'archive_name_audit.py'), str(zip_path)],
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    return proc.returncode == 0


def build(dry_run=False, name=None, out_dir=None, edition='full'):
    cfg, eds = config_for()
    out_dir = Path(out_dir) if out_dir else DIST
    names = [e['name'] for e in eds.zip_editions()] if edition == 'all' else [edition]
    roots = {n: (name if (name and n == 'full') else root_folder(cfg, eds.get(n))) for n in names}
    lines = ['RELEASE PACKAGE REPORT', '=' * 72,
             'timestamp: %s' % time.strftime('%Y-%m-%d %H:%M:%S'),
             'package_root: %s' % ROOT, 'package_id: %s' % cfg['package_id'],
             'editions: %s' % ', '.join(names), 'output: %s' % out_dir, 'dry_run: %s' % dry_run, '']
    errors, warnings = [], []
    if ROOT.name not in roots.values():
        warnings.append('working-copy folder %r differs from the release root %r; the archive uses %r '
                        '(clone folder names are a working-copy convention, the package_id is the '
                        'handoff identity)' % (ROOT.name, roots[names[0]], roots[names[0]]))
    if dry_run:
        lines.append('PASS dry run: naming resolved without writing archives')
        for n in names:
            lines.append('PASS archive %s.zip would unpack to %s/' % (roots[n], roots[n]))
    else:
        if edition == 'all':
            cmd_zips('all', str(out_dir), False)
        else:
            staged = stage_edition(Tree.from_disk(), cfg, eds, edition)
            write_zip(out_dir / (roots[edition] + '.zip'),
                      [('%s/%s' % (roots[edition], rel), data) for rel, data in staged.files.items()],
                      cfg['last_updated'])
        for n in names:
            zip_path = out_dir / (roots[n] + '.zip')
            if zip_roots(zip_path) == [roots[n]] and archive_name_audit(zip_path):
                lines.append('PASS %s: single root %s/ and archive_name_audit passes' % (zip_path.name, roots[n]))
            else:
                errors.append('%s: root or archive_name_audit mismatch (roots %r)' % (zip_path.name, zip_roots(zip_path)))
    lines += ['', 'SUMMARY', '-' * 72, 'SUMMARY: %s' % ('FAIL' if errors else 'PASS')]
    lines += ['WARNING: %s' % w for w in warnings]
    lines += ['ERROR: %s' % e for e in errors]
    text = '\n'.join(lines) + '\n'
    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text(text, encoding='utf-8')
    print(text)
    return (1 if errors else 0), out_dir


def main(argv=None):
    ap = argparse.ArgumentParser(description='Build AISOP release archives')
    ap.add_argument('--dry-run', action='store_true', help='resolve names only; write no archive')
    ap.add_argument('--edition', default='full', choices=['full', 'method', 'chatkit', 'all'],
                    help='which archive to build (default: full; all also writes the card and checksums)')
    ap.add_argument('--name', help='override the Full archive root and basename (default: package_id)')
    ap.add_argument('--out', help='output directory (default: dist/)')
    args = ap.parse_args(argv)
    code, _ = build(args.dry_run, args.name, args.out, args.edition)
    return code


if __name__ == '__main__':
    sys.exit(main())
