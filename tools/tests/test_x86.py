"""Disassembly and xref tests.

Skipped as a whole when capstone is absent - that is the whole point of keeping
it an optional dependency.  When it is present, these are the regression net
for the two bugs the old tools had: a REX-prefix-only xref scan that missed
real references, and decoding that started at a guessed mid-function address.
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
from cubelib.pe import PE                             # noqa: E402
from cubelib import x86                               # noqa: E402

HAVE_CAPSTONE = x86.have_capstone()
requires_capstone = unittest.skipUnless(
    HAVE_CAPSTONE, 'capstone not installed (pip install -r requirements-dev.txt)')


@requires_capstone
class TestDisasm(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.blob, cls.layout = fixture_pe.build()
        cls.tmp = tempfile.TemporaryDirectory()
        cls.path = os.path.join(cls.tmp.name, 'fixture.exe')
        with open(cls.path, 'wb') as fh:
            fh.write(cls.blob)
        cls.pe = PE(cls.path)
        cls.dis = x86.Disassembler(cls.pe)

    @classmethod
    def tearDownClass(cls):
        cls.pe.close()
        cls.tmp.cleanup()

    def test_decodes_lea_with_rex(self):
        insns, fn, _ = self.dis.disasm(self.layout['funcA_off'])
        mnemonics = [i.mnemonic for i in insns]
        self.assertIn('lea', mnemonics)
        self.assertIn('call', mnemonics)
        self.assertIn('ret', mnemonics)

    def test_snaps_to_function_start(self):
        L = self.layout
        # ask for an address in the middle of func A
        mid = L['funcA_off'] + 0x0D
        insns, fn, snapped = self.dis.disasm(mid)
        self.assertTrue(snapped)
        self.assertEqual(fn[0], L['funcA_rva'])
        self.assertEqual(insns[0].address, self.pe.imagebase + L['funcA_rva'])

    def test_annotations_name_the_target_string(self):
        insns, _fn, _ = self.dis.disasm(self.layout['funcA_off'])
        notes = [i.note for i in insns if i.note]
        self.assertTrue(any('Hello from rdata' in n for n in notes), notes)
        self.assertTrue(any('Wide string' in n for n in notes), notes)

    def test_no_annotation_for_unmapped_target(self):
        notes = [i.note for i in self.dis.disasm(self.layout['funcC_off'])[0]]
        self.assertTrue(all('unmapped' not in n for n in notes))

    def test_function_decodes_exactly_one_function(self):
        insns, fn = self.dis.function(self.layout['funcA_rva'])
        self.assertEqual(fn, (self.layout['funcA_rva'],
                              self.layout['funcA_rva'] + 0x20))
        last = insns[-1]
        self.assertLess(last.address, self.pe.imagebase + fn[1])

    def test_format_reports_function_boundary(self):
        out = self.dis.format(self.layout['funcB_off'], 0x20)
        self.assertIn('.pdata function', out)

    def test_format_warns_when_uncovered(self):
        out = self.dis.format(self.pe.rva_to_off(0x2000), 0x10)
        self.assertIn('decoding linearly', out)


@requires_capstone
class TestXref(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.blob, cls.layout = fixture_pe.build()
        cls.tmp = tempfile.TemporaryDirectory()
        cls.path = os.path.join(cls.tmp.name, 'fixture.exe')
        with open(cls.path, 'wb') as fh:
            fh.write(cls.blob)
        cls.pe = PE(cls.path)
        cls.finder = x86.XrefFinder(cls.pe)

    @classmethod
    def tearDownClass(cls):
        cls.pe.close()
        cls.tmp.cleanup()

    def test_finds_all_references_to_a_string(self):
        # func A (REX.W lea) and func B (no-REX lea) both point at the string
        hits = self.finder.find(self.layout['hello_off'])
        self.assertEqual(len(hits), 2, [(hex(h.insn_address)) for h in hits])
        funcs = sorted(h.func_rva[0] for h in hits)
        self.assertEqual(funcs, sorted([self.layout['funcA_rva'],
                                        self.layout['funcB_rva']]))

    def test_finds_non_rex_reference(self):
        # the whole point: a REX-only scanner would report one hit, not two
        hits = self.finder.find(self.layout['hello_off'])
        in_b = [h for h in hits if h.func_rva[0] == self.layout['funcB_rva']]
        self.assertEqual(len(in_b), 1)

    def test_xrefs_carry_function_boundaries(self):
        for h in self.finder.find(self.layout['wide_off']):
            self.assertIsNotNone(h.func_rva)
            self.assertEqual(h.func_rva[1] - h.func_rva[0], 0x20)

    def test_no_references_to_unused_data(self):
        # .rdata beyond the two strings is never referenced
        self.assertEqual(self.finder.find(self.layout['rdata_off'] + 0x800), [])

    def test_out_of_range_target(self):
        self.assertEqual(self.finder.find(self.pe.bin.size + 100), [])

    def test_callers(self):
        target = self.pe.imagebase + self.layout['funcC_rva']
        hits = self.finder.callers(target)
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0].func_rva[0], self.layout['funcA_rva'])


class TestOptionalDependency(unittest.TestCase):
    def test_import_never_fails(self):
        import importlib
        m = importlib.import_module('cubelib.x86')
        self.assertTrue(hasattr(m, 'MissingCapstone'))

    def test_have_capstone_returns_bool(self):
        self.assertIn(x86.have_capstone(), (True, False))

    def test_require_capstone_error_is_actionable(self):
        if HAVE_CAPSTONE:
            self.skipTest('capstone installed')
        with self.assertRaises(x86.MissingCapstone) as ctx:
            x86.require_capstone()
        self.assertIn('requirements-dev.txt', str(ctx.exception))


if __name__ == '__main__':
    unittest.main()
