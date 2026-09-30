"""Put `tools/` on sys.path so research scripts can `import cubelib`.

Importing this module for its side effect is intentional:

    import _bootstrap  # noqa: F401
    from cubelib.pe import PE

Keeps every research script runnable as `python tools/research/foo.py` with no
install step and no packaging ceremony.

It also un-shadows the standard library
----------------------------------------
Running a script from this directory puts the directory at `sys.path[0]`, ahead
of the standard library, so any file here named after a stdlib module wins every
`import` of that name.  `dis.py` did, and the symptom was not a missing module -
it was a circular import that looked like a broken `cubelib`:

    cubelib.pe -> dataclasses -> inspect -> import dis
               -> tools/research/dis.py -> cubelib.pe (half-built) -> ImportError

Scripts here are deliberately short-named one-liners, so `dis.py` is a name worth
expecting again (`code.py`, `types.py`, `struct.py` are all plausible next).
Rather than rely on nobody picking a colliding name, load the real stdlib module
under the plain name before anything else imports it.  Renaming the file is still
the better fix - this only protects scripts that import `_bootstrap`.
"""
import importlib.util
import os
import sys

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)

_HERE = os.path.dirname(os.path.abspath(__file__))
_STDLIB = os.path.dirname(os.__file__)


def _unshadow_stdlib():
    """Pre-import any stdlib module this directory has a same-named file for."""
    try:
        listing = os.listdir(_HERE)
    except OSError:                                   # pragma: no cover
        return
    for name in listing:
        mod, ext = os.path.splitext(name)
        if ext != '.py' or mod.startswith('_'):
            continue
        if mod in sys.modules or mod in sys.builtin_module_names:
            continue
        real = os.path.join(_STDLIB, mod + '.py')
        if not os.path.isfile(real):
            continue
        try:
            spec = importlib.util.spec_from_file_location(mod, real)
            loaded = importlib.util.module_from_spec(spec)
            sys.modules[mod] = loaded                # before exec: it may recurse
            spec.loader.exec_module(loaded)
        except Exception:                             # pragma: no cover
            sys.modules.pop(mod, None)


_unshadow_stdlib()


def die(msg, code=2):
    print(f'error: {msg}', file=sys.stderr)
    raise SystemExit(code)


def need_argv(n, usage):
    if len(sys.argv) < n:
        die(f'expected {n - 1} argument(s)\nusage: {usage}')
