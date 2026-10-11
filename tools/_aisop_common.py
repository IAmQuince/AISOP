#!/usr/bin/env python
"""Shared helpers for AISOP tools (standard library only).

One place for: the package root, config loading, the document-control
front-matter parser, the git-ignore-aware file walk, hashing, and
deterministic zip writing. Every tool that walks the tree or reads a header
imports from here so two tools never disagree about which files exist.
"""
from __future__ import print_function

import fnmatch
import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / 'config' / 'package_metadata.json'
EDITIONS_PATH = ROOT / 'config' / 'editions.json'

# Directories that are never part of the package, whatever .gitignore says.
ALWAYS_SKIP_DIRS = {'.git', 'dist', '__pycache__', '.pytest_cache', '.mypy_cache', '.ruff_cache'}

# The closing '---' of a document-control header must appear within this window.
FRONTMATTER_WINDOW = 4096


# ---------------------------------------------------------------------------
# Text and config
# ---------------------------------------------------------------------------

def read_text(path):
    return Path(path).read_text(encoding='utf-8')


def load_json(path):
    return json.loads(read_text(path))


def load_config(root=None):
    return load_json((Path(root) if root else ROOT) / 'config' / 'package_metadata.json')


def load_editions(root=None):
    return load_json((Path(root) if root else ROOT) / 'config' / 'editions.json')


# ---------------------------------------------------------------------------
# Document-control front matter
# ---------------------------------------------------------------------------

def split_frontmatter(text):
    """Return (header_text, body) or (None, text) when no header is present."""
    if not text.startswith('---\n'):
        return None, text
    end = text.find('\n---\n', 4)
    if end == -1 or end > FRONTMATTER_WINDOW:
        return None, text
    return text[4:end], text[end + 5:]


def _parse_value(value):
    value = value.strip()
    if value.startswith('[') and value.endswith(']'):
        return [item.strip().strip('"\'') for item in value[1:-1].split(',') if item.strip()]
    return value.strip('"')


def parse_frontmatter(text):
    """Parse `key: value` lines; inline `[a, b]` lists become Python lists."""
    header, _ = split_frontmatter(text)
    if header is None:
        return {}
    result = {}
    for line in header.splitlines():
        if ':' in line and not line.startswith((' ', '\t', '#')):
            key, value = line.split(':', 1)
            result[key.strip()] = _parse_value(value)
    return result


# ---------------------------------------------------------------------------
# Git-ignore-aware file walk (works without git, so zip recipients get the
# same file list as clone users)
# ---------------------------------------------------------------------------

def _load_ignore_patterns(root):
    path = Path(root) / '.gitignore'
    patterns = []
    if not path.is_file():
        return patterns
    for raw in read_text(path).splitlines():
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        negate = line.startswith('!')
        if negate:
            line = line[1:]
        dir_only = line.endswith('/')
        line = line.rstrip('/')
        anchored = '/' in line
        segments = line.lstrip('/').split('/')
        patterns.append((segments, negate, dir_only, anchored))
    return patterns


def _match_segments(pattern, parts):
    if not pattern:
        return not parts
    if pattern[0] == '**':
        return any(_match_segments(pattern[1:], parts[i:]) for i in range(len(parts) + 1))
    return bool(parts) and fnmatch.fnmatchcase(parts[0], pattern[0]) and \
        _match_segments(pattern[1:], parts[1:])


def _ignored_state(parts, is_dir, patterns):
    state = False
    for segments, negate, dir_only, anchored in patterns:
        if dir_only and not is_dir:
            continue
        if anchored:
            hit = _match_segments(segments, parts)
        else:
            hit = fnmatch.fnmatchcase(parts[-1], segments[0])
        if hit:
            state = not negate
    return state


def is_ignored(rel_path, patterns, is_dir=False):
    """Git semantics for the subset AISOP uses: an ignored ancestor directory wins."""
    parts = Path(rel_path).parts
    for i in range(1, len(parts) + 1):
        last = i == len(parts)
        if _ignored_state(parts[:i], is_dir if last else True, patterns):
            return True
    return False


def iter_package_files(root=None):
    """Yield every package file (sorted Paths), skipping ALWAYS_SKIP_DIRS and git-ignored files."""
    root = Path(root) if root else ROOT
    patterns = _load_ignore_patterns(root)
    for path in sorted(root.rglob('*')):
        rel = path.relative_to(root)
        if any(part in ALWAYS_SKIP_DIRS for part in rel.parts):
            continue
        if not path.is_file():
            continue
        if is_ignored(rel.as_posix(), patterns):
            continue
        yield path


def rel_posix(path, root=None):
    return Path(path).relative_to(Path(root) if root else ROOT).as_posix()


# ---------------------------------------------------------------------------
# Hashing and deterministic zips
# ---------------------------------------------------------------------------

def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha256_file(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as handle:
        for block in iter(lambda: handle.read(65536), b''):
            h.update(block)
    return h.hexdigest()


def zip_date(iso_date):
    """'2026-10-11' -> zip date tuple; zip cannot store dates before 1980."""
    year, month, day = (int(x) for x in iso_date.split('-'))
    return (max(year, 1980), month, day, 0, 0, 0)


def write_zip(zip_path, members, date_iso):
    """Write members [(arcname, bytes)] sorted by arcname with fixed metadata.

    Fixed timestamps and attributes make the member list and contents
    reproducible; the compressed bytes may still vary with the zlib build.
    """
    zip_path = Path(zip_path)
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    when = zip_date(date_iso)
    with zipfile.ZipFile(str(zip_path), 'w', compression=zipfile.ZIP_DEFLATED) as handle:
        for arcname, data in sorted(members, key=lambda item: item[0]):
            info = zipfile.ZipInfo(arcname, date_time=when)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            info.create_system = 3
            handle.writestr(info, data)
    return zip_path


def zip_roots(zip_path):
    with zipfile.ZipFile(str(zip_path), 'r') as handle:
        return sorted({name.split('/')[0] for name in handle.namelist() if '/' in name})
