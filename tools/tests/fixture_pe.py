"""Build a small but structurally valid PE32+ image for the test suite.

The tests must be runnable without a 135 MB Cubase install, so this
synthesises just enough of a PE for `cubelib.pe` to do real work: DOS header,
COFF header, optional header, three sections, a resource tree, a `.pdata`
function table, and `.text` bytes containing instructions with known
RIP-relative references.

Instructions are assembled by hand so the expectations in the tests are exact
rather than "whatever capstone produced".
"""
import struct
import zlib

DOS = b'MZ' + b'\x00' * 0x3A + struct.pack('<I', 0x40)
STUB = b'PE\x00\x00'

SECTIONS = [
    # name, vaddr, vsize, data
    ('.text',  0x1000, 0x1000, None),   # filled in by build()
    ('.rdata', 0x2000, 0x1000, None),
    ('.rsrc',  0x3000, 0x1000, None),
]

IMAGE_BASE = 0x140000000
FILE_ALIGN = 0x200
SECT_ALIGN = 0x1000


def align_up(v, a):
    return (v + a - 1) // a * a


# --- instructions ---------------------------------------------------------
# 48 8D 05 <disp32>          lea rax, [rip+disp]
# 48 8D 0D <disp32>          lea rcx, [rip+disp]
# E8 <rel32>                 call rel32
# C3                        ret
# CC CC ...                  int3 padding between functions


def lea_rax(target_va, next_va):
    return b'\x48\x8D\x05' + struct.pack('<i', target_va - next_va)


def lea_rcx(target_va, next_va):
    return b'\x48\x8D\x0D' + struct.pack('<i', target_va - next_va)


def call_va(target_va, next_va):
    return b'\xE8' + struct.pack('<i', target_va - next_va)


def int3(n=1):
    return b'\xCC' * n


def build():
    """Return (pe_bytes, layout) where layout describes the known addresses."""
    text_va = IMAGE_BASE + 0x1000
    rdata_va = IMAGE_BASE + 0x2000
    rsrc_va = IMAGE_BASE + 0x3000

    # ---- rdata: two plain strings the .text will reference
    # Pre-allocated: assigning to an out-of-range slice of a bytearray clamps
    # to the end, which silently relocates the data.
    hello = b'Hello from rdata\x00'
    wide = 'Wide string'.encode('utf-16-le') + b'\x00\x00'
    rdata = bytearray(0x1000)
    hello_off = 0
    rdata[hello_off:hello_off + len(hello)] = hello
    wide_off = 0x100
    rdata[wide_off:wide_off + len(wide)] = wide

    # ---- text: three functions
    # Displacements are computed from the address of the *following*
    # instruction, which is what RIP-relative addressing is relative to.
    def va(rva):
        return IMAGE_BASE + rva

    fA_rva = 0x1000
    fB_rva = 0x1020
    fC_rva = 0x1040
    SIZE = 0x20

    leaA_rva = fA_rva                      # 48 8D 05 disp32 -> 7 bytes
    leaW_rva = leaA_rva + 7                # 48 8D 0D disp32 -> 7 bytes
    call_rva = leaW_rva + 7                # E8 rel32        -> 5 bytes

    fA = lea_rax(rdata_va + hello_off, va(leaA_rva + 7))
    fA += lea_rcx(rdata_va + wide_off, va(leaW_rva + 7))
    fA += call_va(va(fC_rva), va(call_rva + 5))
    fA += b'\xC3'
    fA = fA.ljust(SIZE, b'\xCC')
    assert len(fA) == SIZE

    # func B: the same reference through a NON-REX encoding
    #   8D 05 <disp32>  lea eax, [rip+disp]
    fB = b'\x8D\x05' + struct.pack(
        '<i', (rdata_va + hello_off) - va(fB_rva + 6)) + b'\xC3'
    fB = fB.ljust(SIZE, b'\xCC')
    assert len(fB) == SIZE

    # func C: no references at all
    fC = b'\x31\xC0\xC3'          # xor eax, eax ; ret
    fC = fC.ljust(SIZE, b'\xCC')
    assert len(fC) == SIZE

    text = fA + fB + fC
    text = text.ljust(SECTIONS[0][2], b'\xCC')

    # ---- pdata: three RUNTIME_FUNCTION entries, lives in .rdata
    pdata_off = 0x200
    pdata = b''.join(struct.pack('<III', rva, rva + SIZE, 0)
                     for rva in (fA_rva, fB_rva, fC_rva))
    rdata[pdata_off:pdata_off + len(pdata)] = pdata

    # ---- rsrc: one named RCDATA leaf, stored uncompressed as real PEs do
    # A resource data entry's OffsetToData is an RVA, not a VA.  The payload
    # lives at file offset offsets[2] + 0x200, i.e. RVA 0x3000 + 0x200.
    #
    # The tree is type -> name -> language -> data, four 16-byte directory
    # headers with 8-byte entries, and a UTF-16LE name string.
    payload = b'<Translation><StringTable/></Translation>'
    leaf_rva = 0x3000 + 0x200

    res = bytearray(0x200)
    ROOT, TYPE, NAMEDIR, LANGDIR = 0x00, 0x20, 0x40, 0x60
    DATA_ENTRY, NAME_STR = 0x80, 0xA0

    def dir_header(at, named, ids):
        struct.pack_into('<HH', res, at + 12, named, ids)

    def entry(at, name_off, target):
        hi = 0x80000000 if name_off & 0x80000000 else 0
        struct.pack_into('<II', res, at, name_off,
                         (hi | target) if target & 0x80000000 else target)

    dir_header(ROOT, 0, 1)
    entry(ROOT + 16, 10, 0x80000000 | TYPE)            # 10 = RT_RCDATA
    dir_header(TYPE, 1, 0)
    entry(TYPE + 16, 0x80000000 | NAME_STR, 0x80000000 | NAMEDIR)
    dir_header(NAMEDIR, 0, 1)
    entry(NAMEDIR + 16, 1031, 0x80000000 | LANGDIR)    # 1031 = en-US
    dir_header(LANGDIR, 0, 1)
    entry(LANGDIR + 16, 1031, DATA_ENTRY)
    struct.pack_into('<IIII', res, DATA_ENTRY, leaf_rva, len(payload), 0, 0)

    name = 'TRANSLATION.XML'.encode('utf-16-le')
    struct.pack_into('<H', res, NAME_STR, len(name) // 2)
    res[NAME_STR + 2:NAME_STR + 2 + len(name)] = name
    rsrc = bytes(res) + payload

    bodies = [bytes(text), bytes(rdata), rsrc]

    # ---- headers
    optsz = 0xF0                                   # PE32+ with 16 directories
    nsec = len(SECTIONS)
    headers_end = 0x40 + 4 + 20 + optsz + nsec * 40
    raw_start = align_up(headers_end, FILE_ALIGN)

    sec_table = bytearray()
    offsets = []
    cur = raw_start
    for (name, va, vsz, _), body in zip(SECTIONS, bodies):
        offsets.append(cur)
        # IMAGE_SECTION_HEADER: name, vsize, vaddr, rawsize, rawptr,
        # relocptr, linenumptr, nrelocs, nlinenums, characteristics
        sec_table += struct.pack('<8sIIIIIIHHI',
                                 name.encode().ljust(8, b'\0'),
                                 vsz, va, len(body), cur, 0, 0, 0, 0,
                                 0x40000040)          # INITIALIZED_DATA|READ
        cur = align_up(cur + len(body), FILE_ALIGN)

    dirs = bytearray(0x80)
    # Data directories hold RVAs too.
    struct.pack_into('<II', dirs, 2 * 8, 0x3000, 0x200)            # Resource
    struct.pack_into('<II', dirs, 3 * 8, 0x2000 + pdata_off, 36)   # Exception

    opt = bytearray(optsz)
    struct.pack_into('<H', opt, 0, 0x20B)
    struct.pack_into('<Q', opt, 24, IMAGE_BASE)
    struct.pack_into('<I', opt, 32, SECT_ALIGN)
    struct.pack_into('<I', opt, 36, FILE_ALIGN)
    struct.pack_into('<I', opt, 108, 16)
    opt[112:112 + 0x80] = dirs

    coff = struct.pack('<HHIIIHH', 0x8664, nsec, 0, 0, 0, optsz, 0x0022)

    out = bytearray()
    out += DOS
    out += STUB
    out += coff
    out += opt
    out += sec_table
    out += b'\x00' * (raw_start - len(out))
    for off, body in zip(offsets, bodies):
        assert len(out) == off, (hex(len(out)), hex(off))
        out += body
        # body is already appended, so pad to the next file-alignment boundary
        # from the current length - not from current + body.
        out += b'\x00' * (align_up(len(out), FILE_ALIGN) - len(out))

    layout = {
        'imagebase': IMAGE_BASE,
        'text_rva': 0x1000, 'text_off': offsets[0],
        'rdata_rva': 0x2000, 'rdata_off': offsets[1],
        'rsrc_rva': 0x3000, 'rsrc_off': offsets[2],
        'funcA_rva': fA_rva, 'funcB_rva': fB_rva, 'funcC_rva': fC_rva,
        'funcA_off': offsets[0] + fA_rva - 0x1000,
        'funcB_off': offsets[0] + fB_rva - 0x1000,
        'funcC_off': offsets[0] + fC_rva - 0x1000,
        'hello_off': offsets[1] + hello_off,
        'wide_off': offsets[1] + wide_off,
        'resource_name': 'TRANSLATION.XML',
        'resource_payload': b'<Translation><StringTable/></Translation>',
        'file_size': len(out),
    }
    return bytes(out), layout
