"""Put `tools/` on sys.path so research scripts can `import cubelib`.

Importing this module for its side effect is intentional:

    import _bootstrap  # noqa: F401
    from cubelib.pe import PE

Keeps every research script runnable as `python tools/research/foo.py` with no
install step and no packaging ceremony.
"""
import os
import sys

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)


def die(msg, code=2):
    print(f'error: {msg}', file=sys.stderr)
    raise SystemExit(code)


def need_argv(n, usage):
    if len(sys.argv) < n:
        die(f'expected {n - 1} argument(s)\nusage: {usage}')
