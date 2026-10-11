#!/usr/bin/env python
"""hello_aisop: count lines, words, and characters in a text file.

    python hello_aisop.py notes.txt        print the counts
    python hello_aisop.py --version
    python hello_aisop.py --smoke-test     self-check; exit 0 on PASS
    python hello_aisop.py --diagnostics    report to paste back to your AI
"""
# 1. Imports and compatibility ------------------------------------------------
from __future__ import print_function

import io
import os
import platform
import sys
import tempfile

# 2. Constants and version information ----------------------------------------
APP_NAME = 'hello_aisop'
VERSION = '0.1.0'

# 3. Paths, settings, and logging: not needed (no settings, prints to stdout).


# 4. Data model and defaults ---------------------------------------------------
def empty_counts():
    return {'lines': 0, 'words': 0, 'characters': 0}


# 5. Storage / load / save -----------------------------------------------------
def load_text(path):
    with io.open(path, encoding='utf-8') as handle:
        return handle.read()


# 6. Scanning / parsing --------------------------------------------------------
def count_text(text):
    counts = empty_counts()
    counts['lines'] = len(text.splitlines())
    counts['words'] = len(text.split())
    counts['characters'] = len(text)
    return counts


# 7. Business logic / actions --------------------------------------------------
def count_file(path):
    return count_text(load_text(path))


# 8. UI / view rendering -------------------------------------------------------
def render(path, counts):
    return '%s: %d lines, %d words, %d characters' % (
        os.path.basename(path), counts['lines'], counts['words'], counts['characters'])


# 9. Diagnostics / smoke tests -------------------------------------------------
def smoke_test():
    checks = [('empty text', count_text(u''), empty_counts()),
              ('two lines', count_text(u'hello aisop\nsecond line\n'),
               {'lines': 2, 'words': 4, 'characters': 24})]
    handle, path = tempfile.mkstemp(suffix='.txt')
    os.close(handle)
    try:
        with io.open(path, 'w', encoding='utf-8') as out:
            out.write(u'one two\nthree\n')
        checks.append(('file round trip', count_file(path), {'lines': 2, 'words': 3, 'characters': 14}))
    finally:
        os.remove(path)
    failures = 0
    for name, got, expected in checks:
        ok = got == expected
        failures += 0 if ok else 1
        print('%s %s' % ('PASS' if ok else 'FAIL', name))
    print('SUMMARY: %s' % ('FAIL' if failures else 'PASS'))
    return 1 if failures else 0


def diagnostics():
    print('%s %s diagnostics' % (APP_NAME, VERSION))
    print('python: %s' % sys.version.split()[0])
    print('platform: %s' % platform.platform())
    print('working directory: %s' % os.getcwd())
    print('script: %s' % os.path.abspath(__file__))
    return smoke_test()


# 10. Main application / entry point ------------------------------------------
def main(argv):
    if '--version' in argv:
        print('%s %s' % (APP_NAME, VERSION))
        return 0
    if '--smoke-test' in argv:
        return smoke_test()
    if '--diagnostics' in argv:
        return diagnostics()
    if len(argv) != 1 or not os.path.isfile(argv[0]):
        print(__doc__.strip())
        return 2
    print(render(argv[0], count_file(argv[0])))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
