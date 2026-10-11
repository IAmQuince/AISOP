#!/usr/bin/env python
"""Build and check AISOP editions from one source tree (docs/166_EDITIONS_AND_TIERS_SOP.md).

    python tools/build_editions.py entry      regenerate AGENTS.md regions, pointer files, card opener
    python tools/build_editions.py index      regenerate docs/index.json and docs/000_DOCUMENTATION_INDEX.md
    python tools/build_editions.py all        entry + index + PACKAGE_MANIFEST.md, repeated until stable
    python tools/build_editions.py zips       write dist/: the edition zips, AISOP_CARD.md, EDITIONS_CHECKSUMS.txt
    python tools/build_editions.py stage --edition method --out DIR   write one staged edition as a folder
    python tools/build_editions.py --check    write nothing; exit 1 on stale generated files, budget
                                              breaches, or unresolved paths inside any edition

Standard library only. Generated committed files carry no timestamps or exact
byte counts, so --check is deterministic.
"""
from __future__ import print_function

import argparse
import hashlib
import sys
from pathlib import Path

from _aisop_common import EDITION_RANKS, ROOT, current_edition, find_region, sha256_bytes, write_zip
from _aisop_editions import (Tree, budget_status, config_for, edition_members, largest, render_card,
                             render_edition_info, root_folder, unresolved_references)
from _aisop_generators import apply_targets, targets
from manifest_update import MANIFEST_REL, render_manifest

DIST = ROOT / 'dist'


# ---------------------------------------------------------------------------
# Generation and staging
# ---------------------------------------------------------------------------

def settle(tree, cfg, eds, groups=('entry', 'index'), only_present=False, manifest=True):
    """Apply generators (and the manifest) until nothing changes; return the changed paths."""
    changed = set()
    for _ in range(4):
        step = set(apply_targets(tree, cfg, eds, groups, only_present))
        if manifest and MANIFEST_REL in tree.files:
            text, _ = render_manifest(cfg, tree.files.items())
            if tree.files[MANIFEST_REL] != text.encode('utf-8'):
                tree.set(MANIFEST_REL, text)
                step.add(MANIFEST_REL)
        if not step:
            break
        changed |= step
    return changed


def stage_edition(tree, cfg, eds, name):
    """In-memory tree of one zip edition, with its own EDITION_INFO.md, index and manifest."""
    members = edition_members(tree, eds, name)
    staged = Tree({rel: tree.files[rel] for rel in members})
    staged.set('EDITION_INFO.md', render_edition_info(cfg, eds, name, members))
    settle(staged, cfg, eds, only_present=True)
    return staged


def content_checksum(root_name, tree):
    h = hashlib.sha256()
    for rel in sorted(tree.files):
        arc = ('%s/%s' % (root_name, rel)).encode('utf-8')
        data = tree.files[rel]
        h.update(b'%d:' % len(arc) + arc + b'\n' + b'%d\n' % len(data))
        h.update(data)
    return h.hexdigest()


def checkable_editions(eds, root=None):
    rank = EDITION_RANKS[current_edition(root)]
    return [e for e in eds.data['editions'] if EDITION_RANKS[e['name']] <= rank]


# ---------------------------------------------------------------------------
# --check
# ---------------------------------------------------------------------------

def check_generated(disk, cfg, eds, out):
    expected = disk.copy()
    full_tree = current_edition(disk.root) == 'full'
    try:
        settle(expected, cfg, eds, only_present=not full_tree, manifest=False)
    except (KeyError, ValueError) as exc:
        out.fail('generation error: %s' % exc)
        return
    stale = [rel for rel in sorted(set(expected.files) | set(disk.files))
             if rel != MANIFEST_REL and expected.files.get(rel) != disk.files.get(rel)]
    for rel in stale:
        for label, source in stale_targets(disk, expected, eds, rel):
            out.fail('stale %s; edit its source %s, then run `python tools/build_editions.py all`' % (label, source))
    if not stale:
        out.ok('every generated file and region is fresh')


def stale_targets(disk, expected, eds, rel):
    """(label, source) for each generated target in `rel` whose content differs from a fresh render."""
    found = []
    for target in targets(eds):
        if target.path != rel:
            continue
        if target.region and rel in disk.files:
            now = find_region(disk.text(rel), target.region)
            fresh = find_region(expected.text(rel), target.region)
            if now is None or fresh is None or now.group('body') != fresh.group('body'):
                found.append(('GENERATED region %r in %s' % (target.region, rel), target.source))
        elif not target.region:
            found.append(('generated file %s' % rel, target.source))
    return found or [('file %s (text outside its GENERATED regions changed during generation)' % rel,
                      'the region markers in that file')]


def check_card(disk, cfg, eds, out):
    card_cfg = eds.data['card']
    if card_cfg['source'] not in disk.files:
        out.fail('card source %s is missing' % card_cfg['source'])
        return
    card = render_card(disk, cfg, eds).encode('utf-8')
    status, fraction = budget_status(len(card), card_cfg['budget_bytes'], eds.data['warn_fraction'])
    out.result(status, 'card %s: %d of %d bytes (%.0f%%)' % (card_cfg['asset'], len(card), card_cfg['budget_bytes'],
                                                          100 * fraction))
    problems = unresolved_references(Tree({card_cfg['asset']: card}), 'card')
    for rel, line, target in problems:
        out.fail('card cites %r (line %d) without a (chat kit edition) or higher marker' % (target, line))


def check_edition(disk, cfg, eds, edition, out, example_roots):
    name = edition['name']
    staged = stage_edition(disk, cfg, eds, name)
    total, budget = staged.total_bytes(), edition.get('budget_bytes')
    status, fraction = budget_status(total, budget, eds.data['warn_fraction'])
    if budget:
        out.result(status, '%s: %d files, %d of %d bytes (%.0f%%), headroom %d bytes'
                   % (name, len(staged.files), total, budget, 100 * fraction, budget - total))
        if status != 'PASS':
            for size, rel in largest(staged):
                out.lines.append('    largest: %8d  %s' % (size, rel))
    else:
        out.ok('%s: %d files, %d bytes (unbudgeted)' % (name, len(staged.files), total))
    max_files = edition.get('max_files')
    if max_files:
        out.result('PASS' if len(staged.files) <= max_files else 'FAIL',
                   '%s: %d files (max_files %d)' % (name, len(staged.files), max_files))
    if edition.get('unique_basenames'):
        seen = {}
        for rel in staged.files:
            if any(rel.startswith(r.rstrip('/') + '/') for r in example_roots):
                continue
            seen.setdefault(rel.rsplit('/', 1)[-1], []).append(rel)
        dupes = {b: p for b, p in seen.items() if len(p) > 1}
        for base, paths in sorted(dupes.items()):
            out.fail('%s: basename %s is not unique: %s' % (name, base, ', '.join(paths)))
        if not dupes:
            out.ok('%s: basenames unique (flat upload safe; example packages upload separately)' % name)
    if name == current_edition(disk.root):
        out.ok('%s: same file set as this tree; its references are checked by tools/edition_audit.py' % name)
        return
    problems = unresolved_references(staged, name, example_roots, eds.data.get('link_check'))
    for rel, line, target in problems:
        out.fail('%s: %s:%d cites %r, which this edition does not contain; ship it, or mark the line '
                 '"(method edition)" / "(full edition)" / "(chat kit edition)"' % (name, rel, line, target))
    if not problems:
        out.ok('%s: every link and backticked repo path resolves inside the edition' % name)


class Output(object):
    def __init__(self):
        self.lines, self.errors, self.warnings = [], [], []

    def result(self, status, msg):
        self.lines.append('%s %s' % (status, msg))
        if status == 'FAIL':
            self.errors.append(msg)
        elif status == 'WARN':
            self.warnings.append(msg)

    def ok(self, msg):
        self.result('PASS', msg)

    def fail(self, msg):
        self.result('FAIL', msg)


def run_check():
    cfg, eds = config_for()
    disk = Tree.from_disk()
    out = Output()
    out.lines += ['BUILD EDITIONS CHECK', '=' * 72, 'package_id: %s' % cfg['package_id'],
                  'tree edition: %s' % current_edition(), '', 'GENERATED FILES', '-' * 72]
    check_generated(disk, cfg, eds, out)
    out.lines += ['', 'EDITIONS', '-' * 72]
    example_roots = cfg.get('example_packages', [])
    for edition in checkable_editions(eds):
        if edition.get('kind') == 'card':
            check_card(disk, cfg, eds, out)
        else:
            check_edition(disk, cfg, eds, edition, out, example_roots)
    out.lines += ['', 'SUMMARY: %s' % ('FAIL' if out.errors else 'PASS')]
    out.lines += ['WARNING: %s' % w for w in out.warnings]
    print('\n'.join(out.lines))
    return 1 if out.errors else 0


# ---------------------------------------------------------------------------
# Writing
# ---------------------------------------------------------------------------

def write_tree_changes(disk, changed):
    for rel in sorted(changed):
        path = ROOT / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(disk.files[rel])
        print('wrote %s' % rel)
    if not changed:
        print('generated files already fresh')


def cmd_generate(groups, manifest):
    cfg, eds = config_for()
    disk = Tree.from_disk()
    write_tree_changes(disk, settle(disk, cfg, eds, groups=groups, manifest=manifest))
    return 0


def cmd_stage(name, out_dir):
    cfg, eds = config_for()
    staged = stage_edition(Tree.from_disk(), cfg, eds, name)
    root = Path(out_dir) / root_folder(cfg, eds.get(name))
    for rel, data in staged.files.items():
        target = root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    print('staged %s edition (%d files) at %s' % (name, len(staged.files), root))
    return 0


def cmd_zips(selected, out_dir, dry_run):
    cfg, eds = config_for()
    disk = Tree.from_disk()
    out_dir = Path(out_dir) if out_dir else DIST
    rows = []
    for edition in eds.data['editions']:
        name = edition['name']
        if selected not in ('all', name):
            continue
        if edition.get('kind') == 'card':
            data = render_card(disk, cfg, eds).encode('utf-8')
            asset = eds.data['card']['asset']
            rows.append((name, asset, 1, len(data), sha256_bytes(data), data))
            continue
        staged = stage_edition(disk, cfg, eds, name)
        folder = root_folder(cfg, edition)
        rows.append((name, folder + '.zip', len(staged.files), staged.total_bytes(),
                     content_checksum(folder, staged), staged))
    lines = []
    for name, filename, count, size, content_sha, payload in rows:
        target = out_dir / filename
        if dry_run:
            print('would write %s (%d files, %d bytes)' % (target, count, size))
            continue
        if isinstance(payload, bytes):
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(payload)
        else:
            folder = filename[:-4]
            write_zip(target, [('%s/%s' % (folder, rel), d) for rel, d in payload.files.items()], cfg['last_updated'])
        file_sha = sha256_bytes(target.read_bytes())
        lines.append('%-8s %-40s %5d %9d %s %s' % (name, filename, count, size, content_sha, file_sha))
        print('wrote %s' % target)
    if not dry_run and selected == 'all':
        checksums = out_dir / 'EDITIONS_CHECKSUMS.txt'
        head = ['# AISOP edition checksums: package %s, version %s' % (cfg['package_id'], cfg['version']),
                '# content-sha256: sha256 over the members sorted by path, each fed as',
                '#   "<len(arcname)>:<arcname>\\n<len(data)>\\n<data>" (AISOP_CARD.md: sha256 of the file).',
                '#   A local `python tools/build_editions.py zips` on the same tag reproduces it.',
                '# file-sha256: sha256 of the file as downloaded; depends on the zlib build, integrity only.',
                '# edition  file  members  bytes  content-sha256  file-sha256']
        checksums.write_text('\n'.join(head + lines) + '\n', encoding='utf-8')
        print('wrote %s' % checksums)
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description='Build and check AISOP editions')
    ap.add_argument('command', nargs='?', choices=['entry', 'index', 'all', 'zips', 'stage', 'check'])
    ap.add_argument('--check', action='store_true', help='verify only (same as the check command)')
    ap.add_argument('--edition', default='all', help='edition name for zips/stage (default: all)')
    ap.add_argument('--out', help='output directory (zips: default dist/)')
    ap.add_argument('--dry-run', action='store_true', help='zips: list what would be written')
    args = ap.parse_args(argv)
    if args.check or args.command == 'check':
        return run_check()
    if args.command == 'entry':
        return cmd_generate(('entry',), manifest=False)
    if args.command == 'index':
        return cmd_generate(('index',), manifest=False)
    if args.command == 'all':
        return cmd_generate(('entry', 'index'), manifest=True)
    if args.command == 'zips':
        return cmd_zips(args.edition, args.out, args.dry_run)
    if args.command == 'stage':
        if args.edition == 'all' or not args.out:
            ap.error('stage needs --edition NAME and --out DIR')
        return cmd_stage(args.edition, args.out)
    ap.print_help()
    return 2


if __name__ == '__main__':
    sys.exit(main())
