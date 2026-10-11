#!/usr/bin/env python
"""Edition model for AISOP (standard library only).

A Tree is a set of package files held in memory (repo-relative path -> bytes),
read from disk or staged for an edition. Membership, staging, budgets and the
per-edition link check all work on Trees, so the repository and every staged
edition are checked by the same code.
"""
from __future__ import print_function

from _aisop_common import (EDITION_RANKS, ROOT, file_banner, glob_match, iter_package_files, iter_references,
                           line_marker_rank, load_config, load_editions, parse_frontmatter, reference_resolves,
                           rel_posix)

CARD_RULES_BEGIN = '<!-- AISOP:RULES:BEGIN -->'
CARD_RULES_END = '<!-- AISOP:RULES:END -->'


class Tree(object):
    """Package files in memory. Paths are repo-relative POSIX strings."""

    def __init__(self, files, root=None):
        self.files = dict(sorted(files.items()))
        self.root = root
        self._headers = {}
        self._dirs = set()
        for rel in self.files:
            parts = rel.split('/')
            for i in range(1, len(parts)):
                self._dirs.add('/'.join(parts[:i]))

    @classmethod
    def from_disk(cls, root=None):
        root = root or ROOT
        return cls({rel_posix(p, root): p.read_bytes() for p in iter_package_files(root)}, root=root)

    def text(self, rel):
        return self.files[rel].decode('utf-8')

    def set(self, rel, data):
        """Add or replace a file (str or bytes) and keep the directory and header caches valid."""
        self.files[rel] = data.encode('utf-8') if isinstance(data, str) else data
        self._headers.pop(rel, None)
        parts = rel.split('/')
        for i in range(1, len(parts)):
            self._dirs.add('/'.join(parts[:i]))

    def copy(self):
        return Tree(dict(self.files), root=self.root)

    def header(self, rel):
        if rel not in self._headers:
            self._headers[rel] = parse_frontmatter(self.text(rel)) if rel.endswith('.md') else {}
        return self._headers[rel]

    def exists(self, rel):
        rel = rel.rstrip('/')
        return rel in self.files or rel in self._dirs or rel in ('', '.')

    def documents(self):
        """Markdown files that carry a document-control header (`.github/` excluded)."""
        return [rel for rel in self.files
                if rel.endswith('.md') and not rel.startswith('.github/') and self.header(rel)]

    def doc_names(self):
        return [rel.split('/', 1)[1] for rel in self.files if rel.startswith('docs/') and rel.count('/') == 1]

    def tier(self, rel):
        try:
            return int(self.header(rel).get('tier', '3'))
        except ValueError:
            return 3

    def total_bytes(self):
        return sum(len(data) for data in self.files.values())


# ---------------------------------------------------------------------------
# Editions config
# ---------------------------------------------------------------------------

class Editions(object):
    def __init__(self, data=None, root=None):
        self.data = data or load_editions(root)
        self.by_name = {e['name']: e for e in self.data['editions']}

    def get(self, name):
        return self.by_name[name]

    def names(self):
        return [e['name'] for e in self.data['editions']]

    def zip_editions(self):
        return [e for e in self.data['editions'] if e.get('kind') == 'zip']

    def includes(self, name):
        """Include globs of this edition and every lower zip edition (inheritance)."""
        rank = EDITION_RANKS[name]
        globs = []
        for edition in self.zip_editions():
            if EDITION_RANKS[edition['name']] <= rank:
                globs += edition.get('include', [])
        return globs

    def opener(self, name):
        return self.data['openers'][name]


def edition_members(tree, editions, name):
    """Sorted repo-relative paths that belong to edition `name` (zip editions)."""
    edition = editions.get(name)
    globs = editions.includes(name)
    members = []
    for rel in tree.files:
        is_doc = rel.endswith('.md') and not rel.startswith('.github/') and bool(tree.header(rel))
        if is_doc and tree.tier(rel) <= edition['tier']:
            members.append(rel)
        elif any(glob_match(g, rel) for g in globs):
            members.append(rel)
    return sorted(members)


def root_folder(cfg, edition):
    return cfg['package_id'] + edition.get('zip_suffix', '')


# ---------------------------------------------------------------------------
# Card
# ---------------------------------------------------------------------------

def rules_block(card_text):
    start = card_text.find(CARD_RULES_BEGIN)
    end = card_text.find(CARD_RULES_END)
    if start == -1 or end == -1 or end < start:
        raise ValueError('docs/001 lacks the %s ... %s markers' % (CARD_RULES_BEGIN, CARD_RULES_END))
    return card_text[start + len(CARD_RULES_BEGIN):end].strip('\n') + '\n'


def render_card(tree, cfg, editions):
    """AISOP_CARD.md: docs/001 without its header and marker comments, plus an identity line."""
    source = editions.data['card']['source']
    _, body = _split_body(tree.text(source))
    lines = [l for l in body.splitlines() if not l.startswith('<!-- ')]
    title_at = next((i for i, l in enumerate(lines) if l.startswith('# ')), 0)
    identity = ('AISOP version %s, package %s. The full documents win on conflict: '
                'https://github.com/IAmQuince/AISOP' % (cfg['version'], cfg['package_id']))
    lines = lines[:title_at + 1] + ['', identity] + lines[title_at + 1:]
    return '\n'.join(lines).strip('\n') + '\n'


def _split_body(text):
    if text.startswith('---\n'):
        end = text.find('\n---\n', 4)
        if end != -1:
            return text[:end + 5], text[end + 5:]
    return '', text


# ---------------------------------------------------------------------------
# EDITION_INFO.md
# ---------------------------------------------------------------------------

def capabilities(name, members):
    """What the holder of this edition can do; sentences only cite files the edition ships."""
    has = set(members).__contains__
    if name == 'chatkit':
        lines = ['Modes: ORIENT and APPLY only. Changing AISOP itself (MODIFY-AISOP) needs the Method Kit.',
                 'There are no AISOP audit tools to run in this edition.']
        if has('tools/aisop_check.py'):
            lines.append('If you can run Python, `tools/aisop_check.py` audits your own package.')
        if has('templates/MANUAL_AUDIT_CHECKLIST.md'):
            lines.append('Without Python, use `templates/MANUAL_AUDIT_CHECKLIST.md` by hand.')
        if any(m.startswith('examples/') for m in members):
            lines.append('If you upload files one by one instead of the zip, upload the files of `examples/` in a '
                         'separate message: they form an example package with its own README_START_HERE.md.')
        return lines
    if name == 'method':
        return ['Modes: ORIENT, APPLY, MODIFY-AISOP. DOMAIN-LOOKUP needs the domain guides, which are in the '
                'Full edition only.',
                'Run `python tools/run_all_audits.py --quiet` first; it passes inside this edition.']
    return ['Modes: all, including DOMAIN-LOOKUP (one domain guide per task, TL;DR first).',
            'Run `python tools/run_all_audits.py --quiet` first.']


def render_edition_info(cfg, editions, name, members):
    edition = editions.get(name)
    folder = root_folder(cfg, edition)
    read_order = [p for p in editions.data['entry_read_order'] if p in members or p == 'EDITION_INFO.md']
    header = [
        '---',
        'document_id: DOC-EDITION-INFO',
        'title: "Edition Info: %s"' % edition['title'],
        'version: %s' % cfg['version'],
        'revision: %s' % cfg['revision'],
        'status: %s' % cfg['status'],
        'last_updated: %s' % cfg['last_updated'],
        'package_id: %s' % cfg['package_id'],
        'machine_reference_prefix: DOC-EDITION-INFO',
        'normative_status: Informative',
        'tier: %d' % edition['tier'],
        'summary: "Which AISOP edition this is, what it contains, the reading order, and the opener."',
        'edition: %s' % name,
        'root_folder: %s' % folder,
        'base_package_id: %s' % cfg['package_id'],
        'source: "%s"' % file_banner('config/editions.json'),
        '---',
        '',
    ]
    body = [
        '# AISOP %s: Edition Info' % edition['title'],
        '',
        file_banner('config/editions.json'),
        '',
        'You are holding the **%s** edition of AISOP %s (package `%s`, folder `%s/`). %s'
        % (edition['title'], cfg['version'], cfg['package_id'], folder, edition['audience']),
        '',
        '## Opener',
        '',
        'Paste this as your first message to the AI:',
        '',
        '> ' + editions.opener(name),
        '',
        '## Reading order',
        '',
        '1. `EDITION_INFO.md` (this file)',
    ]
    body += ['%d. `%s`' % (i, p) for i, p in enumerate([p for p in read_order if p != 'EDITION_INFO.md'], 2)]
    body += ['', '## What this edition can do', '']
    body += ['- ' + line for line in capabilities(name, members)]
    body += ['- Higher editions are strict supersets with the same file names and IDs; the full documents '
             'win on conflict.', '', '## Files in this edition (%d)' % (len(members) + 1), '']
    body += ['- `%s`' % p for p in sorted(set(members) | {'EDITION_INFO.md'})]
    return '\n'.join(header + body) + '\n'


# ---------------------------------------------------------------------------
# Per-edition link check and budgets
# ---------------------------------------------------------------------------

def unresolved_references(tree, edition_name, example_roots=(), link_check=None):
    """[(path, line_no, target)] for references that do not resolve inside `tree`.

    A line carrying an edition marker for a higher edition than `edition_name`
    is exempt here (the cited file is not shipped in this edition by design).
    `link_check` (from config/editions.json) names planning records, which are
    never checked, and history records, which are checked in the full tree only.
    """
    rank = EDITION_RANKS[edition_name]
    link_check = link_check or {}
    skip = set(link_check.get('planning_records', []))
    if rank < EDITION_RANKS['full']:
        skip |= set(link_check.get('history_records', []))
    doc_names = tree.doc_names()
    problems = []
    for rel in tree.files:
        if not rel.endswith('.md') or rel in skip:
            continue
        bases = [r for r in example_roots if rel.startswith(r.rstrip('/') + '/')]
        for number, kind, target, line in iter_references(tree.text(rel)):
            if line_marker_rank(line) > rank:
                continue
            if not reference_resolves(kind, target, rel, tree.exists, doc_names, extra_bases=bases):
                problems.append((rel, number, target))
    return problems


def budget_status(total, budget, warn_fraction):
    if not budget:
        return 'PASS', None
    fraction = float(total) / budget
    if fraction >= 1.0:
        return 'FAIL', fraction
    if fraction >= warn_fraction:
        return 'WARN', fraction
    return 'PASS', fraction


def largest(tree, count=5):
    return sorted(((len(d), rel) for rel, d in tree.files.items()), reverse=True)[:count]


def config_for(root=None):
    return load_config(root), Editions(root=root)
