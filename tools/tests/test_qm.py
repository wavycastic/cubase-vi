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
                        BLOCK_HASHES, BLOCK_MESSAGES, BLOCK_CONTEXTS,
                        build_catalogue, elf_hash, encode_utf16be,
                        group_messages, message_parts, translate)


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
        # the hash table is a flat (hash, offset) array with one entry per
        # message and no slack, so its length is the entry count
        qm = QM.loads(fixture_qm.catalogue([('A', 'a')] * 9))
        self.assertEqual(qm.hash_slots, 9)
        self.assertEqual(qm.expected_messages, 9)
        self.assertTrue(qm.complete)

    def test_incomplete_is_reported(self):
        # a hash table claiming more entries than the Messages block holds
        raw = fixture_qm.message('A', 'a', 'D')
        qm = QM.loads(fixture_qm.catalogue([], raw_messages=raw, pad_entries=9))
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


class TestRealCatalogues(unittest.TestCase):
    """These only run where a Cubase install exists; they are the regression
    net for the real files."""

    @classmethod
    def setUpClass(cls):
        from cubelib.cubase import Install
        cls.l10n = Install().scoring_l10n
        if not os.path.isdir(cls.l10n):
            raise unittest.SkipTest('no Cubase install')
        cls.files = [os.path.join(cls.l10n, f) for f in sorted(os.listdir(cls.l10n))
                     if f.endswith('.qm')]

    def test_every_catalogue_parses_completely(self):
        bad = []
        for f in self.files:
            qm = QM.load(f)
            if not qm.complete:
                bad.append(f'{f}: {len(qm.messages)}/{qm.expected_messages}')
        self.assertEqual(bad, [], 'incomplete catalogues: ' + '; '.join(bad))

    def test_every_catalogue_roundtrips_byte_for_byte(self):
        """The writer must be an exact `lrelease`.

        This is the load-bearing test of the whole Score Editor pipeline: it
        is what proves we can author `strings_vi.qm` and be confident the
        engine will read it, rather than merely producing a file that parses.
        """
        bad = []
        for f in self.files:
            orig = open(f, 'rb').read()
            out = QM.load(f).dump()
            if out != orig:
                n = min(len(out), len(orig))
                d = next((i for i in range(n) if out[i] != orig[i]), n)
                bad.append(f'{os.path.basename(f)}: {len(orig)} -> {len(out)} '
                           f'bytes, first diff at 0x{d:X}')
        self.assertEqual(bad, [], 'non-identical re-serialisation: '
                                  + '; '.join(bad))

    def test_dump_is_stable(self):
        """Re-serialising twice must be a fixed point, not a slow drift."""
        for f in self.files:
            once = QM.load(f).dump()
            self.assertEqual(QM.loads(once).dump(), once,
                             f'{os.path.basename(f)} is not a fixed point')

    def test_lookup_matches_the_message_stream(self):
        """`lookup` must agree with the record stream for every message.

        Three Qt behaviours make the naive expectation wrong and all three are
        worth pinning down:
          * an empty Tag_Translation is a null QString, i.e. "not found"
          * the hash covers source+comment, so a message whose stored comment
            is non-empty is unreachable from a caller passing comment=""
          * when the same (context, source, comment) appears twice the *earlier*
            record wins, because surviving offsets are scanned in ascending
            order
        """
        for f in self.files:
            cat = QM.load(f)
            if not cat.messages:
                continue
            expected = {}
            for group in group_messages(cat.records):
                trs, src, ctx, cmt = message_parts(group)
                key = (decode_8bit(src), decode_8bit(ctx), decode_8bit(cmt))
                if key not in expected:
                    expected[key] = (decode_utf16(trs[0])
                                     if trs and trs[0] else None)
            for (src, ctx, cmt), want in expected.items():
                if not src:
                    continue
                self.assertEqual(cat.lookup(ctx, src, cmt), want,
                                 f'{os.path.basename(f)}: {ctx!r}/{src!r}'
                                 f'/{cmt!r}')

    def test_comment_disambiguates_repeated_sources(self):
        """The 70 comment-carrying messages are a real, deliberate design.

        Steinberg's Score Editor stores several entries that differ only by
        translator comment, and only the one whose comment matches is reachable.
        Collapsing them would silently drop strings from the Score Editor.
        """
        cat = QM.load(os.path.join(self.l10n, 'strings_zh.qm'))
        commented = [(decode_8bit(src), decode_8bit(ctx), decode_8bit(cmt))
                     for group in group_messages(cat.records)
                     for _, src, ctx, cmt in [message_parts(group)] if cmt]
        self.assertEqual(len(commented), 70)
        pairs = {(s, c) for s, c, _ in commented}
        self.assertLess(len(pairs), len(commented),
                        'comments should be sharing a source within a context')
        # and the reverse: with the wrong comment, nothing resolves
        for src, ctx, cmt in commented[:20]:
            self.assertIsNotNone(cat.lookup(ctx, src, cmt))

    def test_translating_preserves_every_other_lookup(self):
        """Rewriting a subset must not disturb the strings we did not touch.

        A different translation is a different length, so every later message
        moves - the hash table has to be rebuilt from scratch, and this is what
        catches it if it is not.
        """
        cat = QM.load(os.path.join(self.l10n, 'strings_zh.qm'))
        before = {}
        for group in group_messages(cat.records):
            trs, src, ctx, cmt = message_parts(group)
            key = (decode_8bit(ctx), decode_8bit(src), decode_8bit(cmt))
            if key in before or not decode_8bit(src):
                continue
            before[key] = decode_utf16(trs[0]) if trs and trs[0] else None
        sample = sorted(before)[::37]
        mapping = {k: f'~~{i}~~' for i, k in enumerate(sample)}
        vi, stats = translate(cat, mapping)
        self.assertEqual(stats['ambiguous'], 0,
                         'the sample should be unambiguous')
        self.assertEqual(stats['hit'], len(mapping))
        self.assertTrue(vi.complete)
        self.assertEqual(len(vi.messages), len(cat.messages))
        for key, want in before.items():
            ctx, src, cmt = key
            got = vi.lookup(ctx, src, cmt)
            expect = mapping.get(key, want)
            self.assertEqual(got, expect, f'{key!r}: {expect!r} != {got!r}')


class TestWriter(unittest.TestCase):
    """Writer behaviour that does not need a Cubase install."""

    def test_roundtrip_of_a_synthetic_catalogue(self):
        pairs = [('Close', 'Đóng'), ('Version', 'Phiên bản'),
                 ('Add', 'Thêm'), ('Delete', 'Xóa')]
        blob = fixture_qm.catalogue(pairs)
        self.assertEqual(QM.loads(blob).dump(), blob)

    def test_build_catalogue_roundtrips(self):
        entries = [('AboutDialog', 'Close', 'Đóng'),
                   ('AboutDialog', 'Version', 'Phiên bản'),
                   ('Steinberg::Steam::DoricoStringTranslator', 'Stem', 'Nốt nhạc')]
        qm = QM.loads(build_catalogue(entries, language='vi_VN'))
        self.assertTrue(qm.complete)
        self.assertEqual(qm.language, 'vi_VN')
        self.assertEqual(len(qm.messages), 3)
        for ctx, src, want in entries:
            self.assertEqual(qm.lookup(ctx, src), want)
        self.assertEqual(qm.dump(), build_catalogue(entries, language='vi_VN'))

    def test_duplicate_sources_are_separable_by_context(self):
        # the hash covers source+comment only, so context disambiguation
        # happens at lookup time and must not be lost
        entries = [('CtxA', 'Close', 'A-Đóng'), ('CtxB', 'Close', 'B-Đóng')]
        qm = QM.loads(build_catalogue(entries))
        self.assertEqual(qm.lookup('CtxA', 'Close'), 'A-Đóng')
        self.assertEqual(qm.lookup('CtxB', 'Close'), 'B-Đóng')

    def test_vietnamese_survives_the_utf16_round_trip(self):
        entries = [('D', 'S', 'Ký hiệu khoá')]
        qm = QM.loads(build_catalogue(entries))
        self.assertEqual(qm.lookup('D', 'S'), 'Ký hiệu khoá')
        self.assertEqual(QM.loads(qm.dump()).lookup('D', 'S'), 'Ký hiệu khoá')

    def test_odd_length_translation_is_rejected(self):
        # Qt drops a translation whose length is odd, i.e. a lone surrogate;
        # refuse it at build time where it is still visible
        with self.assertRaises(QMError):
            encode_utf16be('\ud800')

    def test_renaming_the_locale_only_touches_the_locale(self):
        pairs = [('Close', 'Đóng')]
        blob = fixture_qm.catalogue(pairs)
        qm = QM.loads(blob)
        out = qm.dump(language='vi_VN')
        self.assertNotEqual(out, blob)
        self.assertEqual(QM.loads(out).language, 'vi_VN')
        self.assertEqual(QM.loads(out).lookup('TestDialog', 'Close'), 'Đóng')

    def test_elf_hash_is_stable_and_never_zero(self):
        self.assertEqual(elf_hash(b''), 1)
        self.assertEqual(elf_hash(b'Close'), elf_hash(b'Close'))
        self.assertNotEqual(elf_hash(b'Close'), elf_hash(b'Close '))
        # source and comment are folded into one accumulator with no separator,
        # so ("ab", "") and ("a", "b") collide - that is Qt's behaviour, and
        # the reason the 70 comment-disambiguated messages exist at all
        self.assertEqual(elf_hash(b'ab', b''), elf_hash(b'a', b'b'))



if __name__ == '__main__':
    unittest.main()
