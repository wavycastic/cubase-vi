#!/usr/bin/env python3
"""Run the whole toolchain test suite.

    python tools/tests/run.py [-v]

Needs neither a Cubase install nor capstone.  The disassembly tests skip
themselves when capstone is not installed, which is deliberate: capstone is an
optional extra so that the translation pipeline stays standard-library only.
"""
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(HERE)
ROOT = os.path.dirname(TOOLS)
for p in (ROOT, TOOLS, HERE):
    if p not in sys.path:
        sys.path.insert(0, p)


def main():
    verbosity = 2 if '-v' in sys.argv else 1
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=HERE, pattern='test_*.py', top_level_dir=TOOLS)
    result = unittest.TextTestRunner(verbosity=verbosity).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    raise SystemExit(main())
