"""cubelib - shared helpers for the cubase-vi toolchain.

Layout
------
    binary.py   mmap-backed file access, string search, hexdump
    pe.py       PE32/PE32+ parsing: sections, RVA<->offset, resources, .pdata
    x86.py      Capstone-backed disassembly and verified xrefs (optional dep)
    qm.py       Qt .qm translation catalogues (Steinberg scoring l10n)
    srf.py      Steinberg Resource File containers (skin.srf)
    cubase.py   Cubase-specific knowledge: install paths, known resources

Only the standard library is required.  `x86` needs capstone, which is an
optional extra:

    pip install -r requirements-dev.txt
"""
__all__ = ['binary', 'pe', 'x86', 'qm', 'srf', 'cubase', 'placeholders']
__version__ = '1.1.0'
