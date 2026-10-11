#!/usr/bin/env python
"""Generated content for AISOP: one registry entry per generated file or region.

Each Target names the file, the region (None for a whole generated file), the
source a human should edit, its group ('entry' or 'index'), and a render
function (tree, cfg, editions) -> str. `apply_targets` returns the new text of
every target, so `build_editions.py` can write them or compare them (--check).
"""
from __future__ import print_function

import json

from _aisop_common import file_banner, replace_region, size_class
from _aisop_editions import rules_block

TIER_TITLES = {0: 'Tier 0: Card', 1: 'Tier 1: Chat Kit', 2: 'Tier 2: Method Kit', 3: 'Tier 3: Full'}


class Target(object):
    def __init__(self, path, region, source, group, render, whole_file_required=False):
        self.path = path
        self.region = region
        self.source = source
        self.group = group
        self.render = render
        self.whole_file_required = whole_file_required

    def label(self):
        return '%s [%s]' % (self.path, self.region) if self.region else self.path


# ---------------------------------------------------------------------------
# Shared pieces
# ---------------------------------------------------------------------------

def generated_header(cfg, document_id, title, tier, summary, source, extra=()):
    lines = [
        '---',
        'document_id: %s' % document_id,
        'title: "%s"' % title,
        'version: %s' % cfg['version'],
        'revision: %s' % cfg['revision'],
        'status: %s' % cfg['status'],
        'last_updated: %s' % cfg['last_updated'],
        'package_id: %s' % cfg['package_id'],
        'machine_reference_prefix: %s' % document_id,
        'normative_status: Informative',
        'tier: %d' % tier,
        'summary: "%s"' % summary,
    ]
    lines += list(extra)
    lines += ['source: "%s"' % file_banner(source), '---', '']
    return '\n'.join(lines) + '\n'


def _escape_cell(text):
    return text.replace('|', '\\|')


# ---------------------------------------------------------------------------
# Entry-layer renders
# ---------------------------------------------------------------------------

def render_agents_rules(tree, cfg, eds):
    return rules_block(tree.text(eds.data['card']['source']))


def render_agents_commands(tree, cfg, eds):
    return ''.join('- `%s`: %s.\n' % (cmd, why) for cmd, why in eds.data['commands'])


def render_card_opener(tree, cfg, eds):
    return '> %s\n' % eds.opener('card')


def _budget_text(edition):
    budget = edition.get('budget_bytes')
    text = '{:,} bytes'.format(budget) if budget else 'unbudgeted'
    if edition.get('max_files'):
        text += ', at most %d files' % edition['max_files']
    return text


def render_editions_table(tree, cfg, eds):
    """Edition table and openers, shown in docs/166 and docs/004 (single source: config/editions.json)."""
    rows = ['| Tier | Edition | Budget | Delivery | Audience |', '|---|---|---|---|---|']
    for e in eds.data['editions']:
        rows.append('| %d | %s | %s | %s | %s |' % (e['tier'], e['title'], _budget_text(e),
                                                   _escape_cell(e['delivery']), _escape_cell(e['audience'])))
    rows += ['', 'Openers (the first message to the AI):', '']
    for e in eds.data['editions']:
        rows.append('- **%s:** %s' % (e['title'], eds.opener(e['name'])))
    return '\n'.join(rows) + '\n'


def make_pointer_render(pointer):
    def render(tree, cfg, eds):
        head = generated_header(cfg, pointer['document_id'], '%s pointer for %s' % (pointer['path'], pointer['tool']),
                                2, 'Pointer that makes %s load AGENTS.md.' % pointer['tool'], 'config/editions.json')
        return (head + '@AGENTS.md\n\n'
                'Read AGENTS.md before doing anything, then follow its first-five-minutes protocol.\n')
    return render


# ---------------------------------------------------------------------------
# Index renders
# ---------------------------------------------------------------------------

def index_records(tree, eds, sizes):
    read_order = {p: i for i, p in enumerate(eds.data['entry_read_order'], 1)}
    records = []
    for rel in tree.documents():
        h = tree.header(rel)
        topics = h.get('topics', [])
        records.append({
            'path': rel,
            'document_id': h.get('document_id', ''),
            'title': h.get('title', ''),
            'size_class': size_class(sizes.get(rel, len(tree.files[rel]))),
            'tier': tree.tier(rel),
            'normative_status': h.get('normative_status', ''),
            'topics': topics if isinstance(topics, list) else [topics],
            'summary': h.get('summary', ''),
            'read_order': read_order.get(rel),
        })
    return sorted(records, key=lambda r: (r['tier'], r['path']))


INDEX_MD = 'docs/000_DOCUMENTATION_INDEX.md'
INDEX_JSON = 'docs/index.json'


def _render_index_md_once(tree, cfg, eds, sizes):
    head = generated_header(cfg, 'DOC-000', 'Documentation Index', 2,
                            'Generated map of every AISOP document by tier, with status, size class, and a one-line summary.',
                            'document-control headers')
    body = ['# Documentation Index', '',
            file_banner('the document-control headers (`tier`, `summary`, `title`, `normative_status`)'), '',
            'Every document carries a `tier`: the lowest edition that includes it. Editions are cumulative, so '
            'the Method Kit holds tiers 0-2 and the Full edition holds everything (`docs/166_EDITIONS_AND_TIERS_SOP.md`). '
            'Size classes: S under 8 KB, M under 24 KB, L under 48 KB, XL larger. The same records, in reading '
            'order, are in `docs/index.json`.', '']
    records = index_records(tree, eds, sizes)
    for tier in sorted({r['tier'] for r in records}):
        body += ['## %s' % TIER_TITLES.get(tier, 'Tier %d' % tier), '',
                 '| Document | Title | Status | Size | Summary |', '|---|---|---|---|---|']
        for r in [r for r in records if r['tier'] == tier]:
            body.append('| `%s` | %s | %s | %s | %s |' % (r['path'], _escape_cell(r['title']), r['normative_status'],
                                                         r['size_class'], _escape_cell(r['summary'])))
        body.append('')
    return head + '\n'.join(body).rstrip('\n') + '\n'


def render_index_md(tree, cfg, eds):
    """Fixed point: the index lists its own size class."""
    sizes = {}
    text = _render_index_md_once(tree, cfg, eds, sizes)
    for _ in range(3):
        sizes[INDEX_MD] = len(text.encode('utf-8'))
        again = _render_index_md_once(tree, cfg, eds, sizes)
        if again == text:
            break
        text = again
    return text


def render_index_json(tree, cfg, eds):
    sizes = {INDEX_MD: len(tree.files[INDEX_MD])} if INDEX_MD in tree.files else {}
    records = index_records(tree, eds, sizes)
    head = {
        'about': ('%s One record per document, ordered by tier then path; read the leading tier 0-1 records '
                  'first. size_class: S < 8 KB, M < 24 KB, L < 48 KB, XL larger.' % file_banner('document-control headers')),
        'package_id': cfg['package_id'],
        'version': cfg['version'],
    }
    lines = ['{']
    lines += ['  %s: %s,' % (json.dumps(k), json.dumps(v)) for k, v in head.items()]
    lines.append('  "documents": [')
    lines += ['    %s%s' % (json.dumps(r, ensure_ascii=False), ',' if i < len(records) - 1 else '')
              for i, r in enumerate(records)]
    lines += ['  ]', '}']
    return '\n'.join(lines) + '\n'


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

def targets(eds):
    card = eds.data['card']['source']
    agents = eds.data['agents_file']['path']
    result = [
        Target(agents, 'rules', card, 'entry', render_agents_rules),
        Target(agents, 'commands', 'config/editions.json', 'entry', render_agents_commands),
        Target(card, 'card-opener', 'config/editions.json', 'entry', render_card_opener),
    ]
    result.append(Target('docs/166_EDITIONS_AND_TIERS_SOP.md', 'editions-table', 'config/editions.json', 'entry',
                         render_editions_table))
    for pointer in eds.data['pointer_files']:
        result.append(Target(pointer['path'], None, 'config/editions.json', 'entry', make_pointer_render(pointer)))
    # Index last: it reads the headers (and sizes) of the files generated above.
    result.append(Target(INDEX_MD, None, 'document-control headers', 'index', render_index_md))
    result.append(Target(INDEX_JSON, None, 'document-control headers', 'index', render_index_json))
    return result


def apply_targets(tree, cfg, eds, groups=('entry', 'index'), only_present=False):
    """Return {path: new_text} after applying every target in `groups` to `tree` (updated in place).

    only_present: skip targets whose file is absent (staged editions that do not ship them).
    Raises KeyError naming the file when a hand-written file lacks a GENERATED region.
    """
    changed = {}
    for target in targets(eds):
        if target.group not in groups:
            continue
        present = target.path in tree.files
        if only_present and not present:
            continue
        if target.region:
            if not present:
                raise KeyError('%s is missing (it must hold the GENERATED region %r)' % (target.path, target.region))
            try:
                text = replace_region(tree.text(target.path), target.region, target.source,
                                      target.render(tree, cfg, eds))
            except KeyError:
                raise KeyError('%s lacks the GENERATED region %r (source: %s)' % (target.path, target.region, target.source))
        else:
            text = target.render(tree, cfg, eds)
        if tree.files.get(target.path) != text.encode('utf-8'):
            tree.set(target.path, text)
            changed[target.path] = text
    return changed
