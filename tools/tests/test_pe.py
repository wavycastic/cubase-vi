"""Tests for cubelib.

    python -m unittest discover -s tools/tests -t tools
    python tools/tests/run.py

Everything here runs against synthetic fixtures, so the suite needs neither a
Cubase install nor capstone for the format parsers.  The disassembly tests skip
themselves when capstone is absent, which is the point of treating it as an
optional dependency.
"""
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(HERE)
for p in (TOOLS, HERE):
    if p not in sys.path:
        sys.path.insert(0, p)

import fixture_pe                                    # noqa: E402
from cubelib.binary import Binary                     # noqa: E402
from cubelib.pe import PE, PEError                   # noqa: E402


class PEFixture(unittest.TestCase):
    """Base class that materialises the synthetic PE once per class."""

    @classmethod
    def setUpClass(cls):
        cls.blob, cls.layout = fixture_pe.build()
        cls.tmp = tempfile.TemporaryDirectory()
        cls.path = os.path.join(cls.tmp.name, 'fixture.exe')
        with open(cls.path, 'wb') as fh:
            fh.write(cls.blob)
        cls.pe = PE(cls.path)

    @classmethod
    def tearDownClass(cls):
        cls.pe.close()
        cls.tmp.cleanup()


class TestHeaders(PEFixture):
    def test_rejects_non_pe(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, 'x.bin')
            open(p, 'wb').write(b'not a pe' * 100)
            with self.assertRaises(PEError):
                PE(p)

    def test_imagebase_and_sections(self):
        L = self.layout
        self.assertEqual(self.pe.imagebase, L['imagebase'])
        self.assertEqual([s.name for s in self.pe.sections],
                         ['.text', '.rdata', '.rsrc'])
        self.assertTrue(self.pe.is_pe32plus)

    def test_offset_rva_roundtrip(self):
        for key in ('funcA_off', 'hello_off', 'rsrc_off'):
            off = self.layout[key]
            rva = self.pe.off_to_rva(off)
            self.assertIsNotNone(rva, key)
            self.assertEqual(self.pe.rva_to_off(rva), off)

    def test_va_roundtrip(self):
        off = self.layout['funcA_off']
        va = self.pe.off_to_va(off)
        self.assertEqual(va, self.pe.imagebase + self.layout['funcA_rva'])
        self.assertEqual(self.pe.va_to_off(va), off)

    def test_resolve_accepts_offset_rva_and_va(self):
        # Use the resource payload: its file offset, RVA and VA are all
        # mutually unambiguous.  (An RVA can collide with some file offset in
        # any given image, and `resolve` deliberately prefers the offset.)
        r = self.pe.find_resource(self.layout['resource_name'])
        self.assertIsNotNone(r)
        rva = self.pe.off_to_rva(r.off)
        va = self.pe.imagebase + rva
        for probe, expect_kind in ((r.off, 'offset'), (rva, 'rva'), (va, 'va')):
            got, kind = self.pe.resolve(probe)
            self.assertEqual(got, r.off)
            self.assertEqual(kind, expect_kind)

    def test_resolve_rejects_out_of_range(self):
        self.assertEqual(self.pe.resolve(0x7FFFFFFF), (None, None))

    def test_unmapped_rva(self):
        self.assertIsNone(self.pe.rva_to_off(0x500000))


class TestFunctions(PEFixture):
    def test_function_count(self):
        self.assertEqual(len(self.pe.functions()), 3)

    def test_function_containing(self):
        L = self.layout
        fn = self.pe.function_containing(L['funcB_rva'])
        self.assertEqual(fn, (L['funcB_rva'], L['funcB_rva'] + 0x20))

    def test_function_containing_gap(self):
        # the three fixture functions are contiguous; past the last one there
        # is no .pdata coverage at all
        self.assertIsNone(self.pe.function_containing(0x1060))
        self.assertIsNone(self.pe.function_containing(0x2000))

    def test_function_containing_off(self):
        fn = self.pe.function_containing_off(self.layout['funcC_off'])
        self.assertEqual(fn[0], self.layout['funcC_rva'])


class TestResources(PEFixture):
    def test_find_named_resource(self):
        r = self.pe.find_resource(self.layout['resource_name'])
        self.assertIsNotNone(r)
        self.assertEqual(r.type_name, 'RCDATA')
        self.assertEqual(pe_bytes_of(self.pe, r), self.layout['resource_payload'])

    def test_resource_bytes_helper(self):
        data = self.pe.resource_bytes(self.layout['resource_name'])
        self.assertEqual(data, self.layout['resource_payload'])

    def test_missing_resource(self):
        self.assertIsNone(self.pe.find_resource('NOPE.XML'))


def pe_bytes_of(pe, res):
    return pe.bin.slice(res.off, res.size)


class TestBinary(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tmp.name, 'b.bin')
        self.data = b'\x00\x01Hello World\x00\xff' + 'WIDE'.encode('utf-16-le') + b'\x00\x00'
        with open(self.path, 'wb') as fh:
            fh.write(self.data)

    def tearDown(self):
        self.tmp.cleanup()

    def test_find_and_cstr(self):
        with Binary(self.path) as b:
            i = b.find(b'World')[0]
            self.assertEqual(b.cstr(i), 'World')
            self.assertEqual(b.cstr(0), '')          # leading NUL
            self.assertIsNone(b.cstr(len(b.data)))

    def test_read_str_wide(self):
        with Binary(self.path) as b:
            i = b.find('WIDE'.encode('utf-16-le'))[0]
            self.assertEqual(b.read_str(i, wide=True), 'WIDE')

    def test_slice_clamps(self):
        with Binary(self.path) as b:
            self.assertEqual(b.slice(len(b.data) - 2, 99), b.data[-2:])

    def test_hexdump_shape(self):
        with Binary(self.path) as b:
            out = b.hexdump(0, 16)
            self.assertEqual(len(out.splitlines()), 1)
            self.assertIn('00000000', out)

    def test_find_limit(self):
        with Binary(self.path) as b:
            self.assertEqual(len(b.find(b'\x00', limit=3)), 3)

    def test_context_manager_closes(self):
        with Binary(self.path) as b:
            size = len(b)
        with self.assertRaises(ValueError):
            b.slice(0, 1)


if __name__ == '__main__':
    unittest.main()
