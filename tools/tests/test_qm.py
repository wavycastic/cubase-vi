import os
import struct
import sys
import unittest
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(HERE)
for p in (TOOLS, HERE):
    if p not in sys.path:
        sys.path.insert(0, p)

import fixture_qm                                    # noqa: E402
from cubelib.qm import (QM, QMError, decode_utf16, decode_8bit,  # noqa: E402
                        BLOCK_HASHES, BLOCK_MESSAGES, BLOCK_CONTEXTS)


class TestDecode(unittest.TestCase):
    def test_utf16_big_endian(self):
        self.assertEqual(decode_utf16('Close'.encode('utf-16-be')), 'Close')

    def test_utf16_little_endian(self):
        self.assertEqual(decode_utf16('Close'.encode('utf-16-le')), 'Close')

    def test_utf16_bom(self):
        self.assertEqual(decode_utf16(b'\xfe\xff' + 'Hi'.encode('utf-16-be')), 'Hi')
        self.assertEqual(decode_utf16(b'\xff\xfe' + 'Hi'.encode('utf-16-le')), 'Hi')

    def test_utf16_surrogate_does_not_raise(self):
        self.assertIsInstance(decode_utf16(b'\x00\xd8\x00\x00'), str)

    def test_utf16_empty(self):
        self.assertEqual(decode_utf16(b''), '')

    def test_8bit_utf8(self):
        self.assertEqual(decode_8bit('Tạo Track'.encode('utf-8')), 'Tạo Track')

    def test_8bit_latin1_fallback(self):
        self.assertEqual(decode_8bit(b'caf\xe9'), 'café')


class TestQM(unittest.TestCase):
    def test_rejects_bad_magic(self):
        with self.assertRaises(QMError):
            QM.loads(b'not a qm file at all............')

    def test_roundtrip_wide(self):
        pairs = [('Close', 'Đóng'), ('Version', 'Phiên bản'), ('Add', 'Thêm')]
        qm = QM.loads(fixture_qm.catalogue(pairs, context='vi_VN'))
        self.assertTrue(qm.complete, 'hash table implies more messages than parsed')
        got = {m.source: m.translation for m in qm.messages if m.source}
        self.assertEqual(got, dict(pairs))
        self.assertEqual(qm.contexts, ['vi_VN'])

    def test_contexts_block_is_unframed_8bit(self):
        # Steinberg's catalogues store the locale as raw bytes with no length
        # prefix, so the reader must not assume one
        blob = fixture_qm.catalogue([('a', 'b')], context='en_US')
        i = blob.find(b'en_US')
        self.assertGreater(i, 0)
        qm = QM.loads(blob)
        self.assertEqual(qm.contexts, ['en_US'])

    def test_contexts_block_with_length_prefix(self):
        # Some catalogues frame each context with a 2-byte code-unit count
        # followed by UTF-16BE.  Build one directly rather than splicing, so
        # the block length stays correct.
        raw = fixture_qm.message('a', 'b', 'D')
        framed = struct.pack('>H', 5) + 'en_US'.encode('utf-16-be')
        out = fixture_qm.MAGIC + fixture_qm.block(0x2F, framed)
        out += fixture_qm.block(0x42, struct.pack('>I', 1))
        out += fixture_qm.block(0x69, raw)
        self.assertEqual(QM.loads(out).contexts, ['en_US'])

    def test_roundtrip_8bit_source_and_context(self):
        # Real catalogues carry the source and context as 8-bit tags (6 and 7)
        # while the translation stays UTF-16, so exercise exactly that mix.
        raw = b''.join(fixture_qm.message(s, t, 'D', wide=False)
                       for s, t in [('Close', 'Close'),
                                    ('Acknowledgements', 'Acknowledgements')])
        qm = QM.loads(fixture_qm.catalogue([], raw_messages=raw))
        self.assertEqual({m.source: m.translation for m in qm.messages},
                         {'Close': 'Close',
                          'Acknowledgements': 'Acknowledgements'})
        self.assertTrue(all(m.context == 'D' for m in qm.messages))

    def test_context_recorded_on_group_start(self):
        # lrelease emits the context once per group, not per message
        qm = QM.loads(fixture_qm.catalogue([('A', 'a'), ('B', 'b')],
                                           context='MyDialog'))
        ctxs = {m.context for m in qm.messages if m.source}
        self.assertEqual(ctxs, {'MyDialog', ''})
        first = next(m for m in qm.messages if m.source)
        self.assertEqual(first.context, 'MyDialog')

    def test_block_lengths_are_big_endian(self):
        blob = fixture_qm.catalogue([('Close', 'Đóng')])
        qm = QM.loads(blob)
        self.assertEqual(qm.consumed, len(blob))
        self.assertIn(BLOCK_MESSAGES, qm.blocks)

    def test_null_translation_sentinel(self):
        # a sentinel record spliced between two real messages must not cost us
        # the ones after it
        raw = (fixture_qm.message('A', 'a', 'D')
               + fixture_qm.sentinel_message()
               + fixture_qm.message('B', 'b')
               + fixture_qm.message('C', 'c'))
        qm = QM.loads(fixture_qm.catalogue([('A', 'a'), ('B', 'b'), ('C', 'c')],
                                           raw_messages=raw))
        sources = [m.source for m in qm.messages if m.source]
        self.assertEqual(sources, ['A', 'B', 'C'])
        # and the sentinel itself carries no translation
        self.assertTrue(any(m.context == 'AboutDi' for m in qm.messages))

    def test_expected_messages_uses_hash_table(self):
        # lrelease sizes the table at exactly 2x the entry count
        qm = QM.loads(fixture_qm.catalogue([('A', 'a')] * 9))
        self.assertEqual(qm.hash_slots, 18)
        self.assertEqual(qm.expected_messages, 9)
        self.assertTrue(qm.complete)

    def test_incomplete_is_reported(self):
        # a Messages block with fewer records than the table implies
        raw = fixture_qm.message('A', 'a', 'D')
        qm = QM.loads(fixture_qm.catalogue([], raw_messages=raw, slots=20))
        self.assertEqual(qm.expected_messages, 10)
        self.assertFalse(qm.complete)

    def test_empty_catalogue(self):
        qm = QM.loads(fixture_qm.catalogue([]))
        self.assertEqual(qm.messages, [])
        self.assertTrue(qm.complete)

    def test_catalogue_dict(self):
        pairs = [('x', 'y'), ('a', 'b')]
        qm = QM.loads(fixture_qm.catalogue(pairs))
        self.assertEqual(qm.catalogue(), dict(pairs))

    def test_pairs_skips_context_only(self):
        qm = QM.loads(fixture_qm.catalogue([('a', 'b')]))
        self.assertEqual(qm.pairs(), [('a', 'b')])


class TestRealCataloguesSkipped(unittest.TestCase):
    """These only run where a Cubase install exists; they are the regression
    net for the real files."""

    @classmethod
    def setUpClass(cls):
        from cubelib.cubase import Install
        cls.l10n = Install().scoring_l10n
        if not os.path.isdir(cls.l10n):
            raise unittest.SkipTest('no Cubase install')

    def test_every_catalogue_parses_completely(self):
        bad = []
        for f in sorted(os.listdir(self.l10n)):
            if not (f.startswith('strings_') or f.startswith('qtbase_')):
                continue
            if not f.endswith('.qm'):
                continue
            qm = QM.load(os.path.join(self.l10n, f))
            if not qm.complete:
                bad.append(f'{f}: {len(qm.messages)}/{qm.expected_messages}')
        self.assertEqual(bad, [], 'incomplete catalogues: ' + '; '.join(bad))


if __name__ == '__main__':
    unittest.main()
