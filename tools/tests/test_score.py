"""Tests for `cubelib.score` - the Score Editor's instrument name file.

The builder edits `instrumentnames_XX.xml` by splicing text into each
`<InstrumentNameEntityDefinition>` block rather than by re-serialising a parsed
tree.  That is not a shortcut, it is the only way to write this file without
changing bytes: the shipped catalogues are CRLF, tab-indented, carry a
`<?xml version="1.0" ?>` header with a space before the `?>`, write empty
fields as `<x/>`, and - in one entity - put their children in a different order
from the other 623.  An ElementTree round trip normalises all of that.

So the tests are about the guarantee that splicing buys: an identity build
reproduces the source byte for byte apart from the language marker, a real
translation changes the five name fields and nothing else, and a value that is
not in the source is reported rather than written.
"""
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(HERE)
ROOT = os.path.dirname(TOOLS)
for p in (TOOLS, HERE):
    if p not in sys.path:
        sys.path.insert(0, p)

import fixture_score                                    # noqa: E402
from cubelib import score                                # noqa: E402

L10N = os.path.join(r'E:\Steinberg\Cubase 15', 'Components',
                    'ScoringEngine', 'l10n')
SHIPPED = os.path.join(L10N, 'instrumentnames_en.xml')


class TempFile(unittest.TestCase):
    """A scratch copy of the fixture, and the built file beside it."""

    def setUp(self):
        self.dir = tempfile.mkdtemp(prefix='score_test_')
        self.src = os.path.join(self.dir, 'instrumentnames_en.xml')
        self.out = os.path.join(self.dir, 'instrumentnames_vi.xml')
        with open(self.src, 'w', encoding='utf-8', newline='') as fh:
            fh.write(fixture_score.DOCUMENT)

    def built(self, mapping=None, **kw):
        report = score.build(self.src, mapping or {}, self.out, **kw)
        with open(self.out, encoding='utf-8', newline='') as fh:
            return report, fh.read()


class TestRead(TempFile):
    def test_entity_count(self):
        text, entities = score.read(self.src)
        self.assertEqual(len(entities), fixture_score.ENTITIES)
        self.assertEqual(text, fixture_score.DOCUMENT)

    def test_localised_fields_only(self):
        _, entities = score.read(self.src)
        for ent in entities:
            self.assertEqual(set(ent.fields), set(score.LOCALISED_FIELDS))
            # `name`, `entityID`, `parentEntityID` and the rest are never
            # translated, so they are not offered to a translator.
            self.assertNotIn('name', ent.fields)
            self.assertNotIn('gender', ent.fields)
            self.assertNotIn('language', ent.fields)

    def test_values_are_unescaped(self):
        _, entities = score.read(self.src)
        bass = [e for e in entities if e.entity_id.endswith('.bass')][0]
        self.assertEqual(bass.fields['uiName'], 'Bass & Violin')
        self.assertEqual(bass.fields['singularShortName'], 'B&V')

    def test_empty_field(self):
        _, entities = score.read(self.src)
        cajon = [e for e in entities if e.entity_id.endswith('.cajon')][0]
        self.assertEqual(cajon.fields['singularShortName'], '')
        self.assertEqual(cajon.fields['pluralShortName'], '')

    def test_trailing_space_preserved(self):
        _, entities = score.read(self.src)
        ondes = [e for e in entities if e.entity_id.endswith('.ondes')][0]
        self.assertEqual(ondes.fields['uiName'], 'Ondes Martenot ')
        self.assertEqual(ondes.fields['singularShortName'], 'O. M. ')

    def test_source_strings_counts_users(self):
        _, entities = score.read(self.src)
        seen = score.source_strings(entities)
        # 6 entities x 5 fields = 30 slots, 2 of them empty in cajon.  Of the
        # 28 that hold text, cajon's three all say `Cajon`, so 16 distinct
        # strings reach the translator.
        self.assertEqual(len(seen), 16)
        self.assertTrue(all(v for v in seen), 'empty value leaked in')
        self.assertTrue(all(u for u in seen.values()), 'entity lost')
        # Users are deduplicated per entity: `uiName` and `singularFullName`
        # hold the same text, and that is one instrument, not two.
        self.assertEqual(sorted({len(u) for u in seen.values()}), [1])
        self.assertEqual(len(seen['Cajon']), 1)

    def test_odd_child_order_is_read(self):
        """`<name>` before `<entityID>` must not confuse the parser."""
        _, entities = score.read(self.src)
        alu = [e for e in entities if e.entity_id.endswith('.aluphone')][0]
        self.assertEqual(alu.fields['uiName'], 'Aluphone')
        self.assertEqual(alu.fields['singularShortName'], 'Alu.')
        # The odd child sits between uiName and singularFullName, and must not
        # be mistaken for one of them.
        self.assertEqual(alu.block.count('<customVariantString/>'), 1)


class TestIdentityBuild(TempFile):
    def test_byte_exact_apart_from_the_language_marker(self):
        _, text = self.built()
        want = score.LANGUAGE.sub(
            f'<language>{score.TARGET_LANGUAGE}</language>',
            fixture_score.DOCUMENT)
        self.assertEqual(text, want)

    def test_every_marker_retagged(self):
        report, text = self.built()
        self.assertEqual(report['language'], score.TARGET_LANGUAGE)
        self.assertEqual(report['language_markers'],
                         fixture_score.LANGUAGE_MARKERS)
        self.assertNotIn('kEnglish', text)

    def test_foreign_marker_reported(self):
        """The aluphone entity is tagged kEnglish in all eight non-English
        catalogues Steinberg ships.  A build normalises it and says so."""
        report, _ = self.built()
        self.assertEqual(report['mis_tagged'], ['kEnglish'])

    def test_line_endings_survive(self):
        _, text = self.built()
        self.assertEqual(text.count('\r\n'), text.count('\n'))
        self.assertGreater(text.count('\r\n'), 0)
        self.assertTrue(text.startswith('<?xml version="1.0" ?>\r\n'))

    def test_untouched_escapes_survive(self):
        _, text = self.built()
        self.assertIn('<singularShortName>B&amp;V</singularShortName>', text)
        self.assertIn('<uiName>Bass &amp; Violin</uiName>', text)

    def test_self_closing_untouched(self):
        _, text = self.built()
        self.assertIn('<singularShortName/>', text)
        self.assertIn('<pluralShortName/>', text)
        self.assertIn('<customVariantString/>', text)


class TestTranslation(TempFile):
    MAP = {'Accordion': 'Đàn accordion',
           'Accordions': 'Đàn accordion',
           'Pianos': 'Đàn piano',
           'Pno': 'Pno',
           'Ondes Martenot ': 'Đàn Ondes Martenot',
           'O. M. ': 'O. M. ',
           'Bass & Violin': 'Đàn bass và violin',
           'Basses & Violins': 'Đàn bass và violin',
           'B&V': 'B&V',
           'Cajon': 'Cajon'}

    def test_replaced_count(self):
        report, _ = self.built(self.MAP)
        # Every slot whose English text is a key, counted the way `build`
        # counts them: accordion 3, piano 3, ondes 5, bass 5, cajon 3.
        self.assertEqual(report['replaced'], 18)

    def test_only_named_fields_change(self):
        """The guarantee that splicing buys: an entity is the English entity
        with the five name fields and `<language>` swapped, and every other
        byte identical."""
        report, text = self.built(self.MAP)
        self.assertIn('<uiName>Đàn accordion</uiName>', text)
        # Structure that is not a name field is untouched, escapes and all.
        self.assertIn('<name>Accordion</name>', text)
        self.assertIn('<parentEntityID/>', text)
        self.assertIn('<inheritanceMask>0</inheritanceMask>', text)
        self.assertIn('<gender>kNeutral</gender>', text)
        self.assertIn('<entities array="true">', text)
        # Indentation survives, which an ElementTree round trip would not.
        self.assertIn('\t\t\t\t\t<gender>kNeutral</gender>\r\n', text)

    def test_vietnamese_reaches_every_slot(self):
        self.built(self.MAP)
        _, entities = score.read(self.out)
        acc = [e for e in entities if e.entity_id.endswith('.accordion')][0]
        self.assertEqual(acc.fields['uiName'], 'Đàn accordion')
        self.assertEqual(acc.fields['singularFullName'], 'Đàn accordion')
        self.assertEqual(acc.fields['pluralFullName'], 'Đàn accordion')
        self.assertEqual(acc.fields['singularShortName'], 'Accord.')
        self.assertEqual(acc.fields['pluralShortName'], 'Accord.')

    def test_untranslated_slot_keeps_english(self):
        self.built(self.MAP)
        _, entities = score.read(self.out)
        acc = [e for e in entities if e.entity_id.endswith('.accordion')][0]
        # `Accord.` was not in the mapping, so the short name is still English
        # and the field is not blanked.
        self.assertEqual(acc.fields['singularShortName'], 'Accord.')

    def test_unused_keys_reported(self):
        report, _ = self.built({'Nonexistent Instrument': 'X'})
        self.assertEqual(report['unused'], ['Nonexistent Instrument'])

    def test_unused_keys_absent_when_all_used(self):
        report, _ = self.built(self.MAP)
        self.assertEqual(report['unused'], [])

    def test_escapes_written_for_a_new_value(self):
        self.built({'Cajon': 'Cajon & Co'})
        with open(self.out, encoding='utf-8', newline='') as fh:
            text = fh.read()
        self.assertIn('<uiName>Cajon &amp; Co</uiName>', text)

    def test_trailing_space_kept_by_an_identity_mapping(self):
        """A source value with a trailing space may map to itself, because an
        identity mapping introduces nothing.  What it may not become is a
        value that carries leading or trailing space of its own - the guard is
        on the result, not on where the text came from."""
        _, text = self.built(self.MAP)
        self.assertIn('<singularShortName>O. M. </singularShortName>', text)
        # Dropping the space is fine - the guard is on the result, not on
        # where the text came from.  Adding one is not.
        for bad in (' O.M.', 'O.M. ', '  '):
            with self.assertRaises(score.ScoreError, msg=bad):
                score.build(self.src, {'O. M. ': bad}, self.out)
        self.assertEqual(score.build(self.src, {'O. M. ': 'O.M.'},
                                     self.out)['replaced'], 2)


class TestGuards(TempFile):
    def test_expect_mismatch(self):
        with self.assertRaises(score.ScoreError):
            score.build(self.src, {}, self.out, expect=99)

    def test_wrong_target_language(self):
        with self.assertRaises(score.ScoreError):
            score.build(self.src, {}, self.out, language='kEnglish')

    def test_control_character_rejected(self):
        with self.assertRaises(score.ScoreError):
            score.build(self.src, {'Piano': 'Pia\x07no'}, self.out)

    def test_replacement_character_rejected(self):
        with self.assertRaises(score.ScoreError):
            score.build(self.src, {'Piano': 'Piano\ufffd'}, self.out)

    def test_surrounding_space_rejected(self):
        with self.assertRaises(score.ScoreError):
            score.build(self.src, {'Piano': ' Piano'}, self.out)

    def test_empty_translation_is_reported_not_silently_blanked(self):
        with self.assertRaises(score.ScoreError):
            score.build(self.src, {'Piano': '   '}, self.out)

    def test_missing_file(self):
        with self.assertRaises(score.ScoreError):
            score.build(os.path.join(self.dir, 'nope.xml'), {}, self.out)


class TestCheckText(unittest.TestCase):
    def test_accepts(self):
        for good in ('Piano', 'Đàn piano', 'Guitar cổ điển', 'Bass 4 dây',
                     'Trống Snare diễu hành, chỉ vành (1 dòng)'):
            self.assertEqual(score.check_text(good, 'k'), good)

    def test_rejects(self):
        for bad, why in (('', 'empty'), ('  ', 'blank'), (' x', 'leading'),
                         ('x ', 'trailing'), ('a\tb\x01', 'control'),
                         ('\ufffd', 'replacement character'),
                         ('\u0111\u00e0n piano\x00', 'null')):
            with self.assertRaises(score.ScoreError, msg=why):
                score.check_text(bad, 'k')

    def test_tabs_and_newlines_allowed(self):
        self.assertEqual(score.check_text('a\tb\nc', 'k'), 'a\tb\nc')


class TestCheckConsistency(unittest.TestCase):
    KNOWN = {'Piano', 'Pianos', 'Cajon', 'Accordion', 'Accordions',
             'Oboe', 'Oboes', 'Basses', 'Bass'}

    def test_clean(self):
        self.assertEqual(score.check_consistency(
            {'Piano': 'Đàn piano', 'Pianos': 'Đàn piano',
             'Accordion': 'Accordion', 'Accordions': 'Accordion'}, self.KNOWN),
            [])

    def test_plural_disagrees_with_singular(self):
        bad = score.check_consistency(
            {'Piano': 'Đàn piano', 'Pianos': 'Piano'}, self.KNOWN)
        self.assertTrue(any('plural differs' in p for p in bad), bad)

    def test_identity_plural_is_exempt(self):
        """An inherited English plural is not this tool's to fix."""
        self.assertEqual(score.check_consistency(
            {'Oboe': 'Oboe', 'Oboes': 'Oboes'}, self.KNOWN), [])

    def test_unknown_key(self):
        self.assertTrue(any('not in' in p for p in score.check_consistency(
            {'Saxofone': 'Sax'}, self.KNOWN)))

    def test_control_character(self):
        self.assertTrue(any('control character' in p
                            for p in score.check_consistency(
                                {'Piano': 'a\x01b'}, self.KNOWN)))

    def test_replacement_character(self):
        self.assertTrue(any('U+FFFD' in p for p in score.check_consistency(
            {'Piano': '\ufffd'}, self.KNOWN)))

    def test_value_may_not_extend_its_key(self):
        """A value that begins with its whole key has grown a word rather
        than replaced it - `Accordion` -> `Accordion dây` reads as a mistake
        where `Guitar cổ điển` does not, because that key is not a prefix."""
        bad = score.check_consistency({'Accordion': 'Accordion dây'},
                                      self.KNOWN)
        self.assertTrue(any('extends its key' in p for p in bad), bad)

    def test_a_translated_value_may_be_anything_else(self):
        """The prefix rule is a mistake-catcher, not a word-order rule:
        `Acoustic Guitar` -> `Guitar acoustic` is a legal rewrite."""
        self.assertEqual(score.check_consistency(
            {'Acoustic Guitar': 'Guitar acoustic'},
            self.KNOWN | {'Acoustic Guitar'}), [])

    def test_value_may_not_drop_a_non_plural_tail(self):
        bad = score.check_consistency({'Accordions': 'Accord'}, self.KNOWN)
        self.assertTrue(any('non-plural tail' in p for p in bad), bad)

    def test_collapse_onto_a_real_singular_is_fine(self):
        self.assertEqual(score.check_consistency(
            {'Basses': 'Bass', 'Bass': 'Bass'}, self.KNOWN), [])

    def test_documented_exception(self):
        """`Voice` is one line and `Voices` is the section that holds them."""
        known = self.KNOWN | {'Voice', 'Voices'}
        self.assertEqual(score.check_consistency(
            {'Voice': 'Bè', 'Voices': 'Các bè'}, known), [])
        # The same disagreement is still reported for any other pair.
        self.assertTrue(score.check_consistency(
            {'Oboe': 'Bè', 'Oboes': 'Các bè'}, self.KNOWN))


class TestShippedFile(unittest.TestCase):
    """The real file, when there is a Cubase install to read it from.

    Skipped otherwise, so the suite still needs neither Cubase nor capstone.
    """

    def setUp(self):
        if not os.path.exists(SHIPPED):
            self.skipTest(f'no ScoringEngine install at {L10N}')

    def test_identity_build_is_exact(self):
        with tempfile.TemporaryDirectory(prefix='score_real_') as d:
            out = os.path.join(d, 'instrumentnames_vi.xml')
            report = score.build(SHIPPED, {}, out)
            with open(SHIPPED, encoding='utf-8', newline='') as fh:
                src = fh.read()
            with open(out, encoding='utf-8', newline='') as fh:
                got = fh.read()
            want = score.LANGUAGE.sub(
                f'<language>{score.TARGET_LANGUAGE}</language>', src)
            self.assertEqual(got, want)
            self.assertEqual(report['entities'], 624)
            self.assertEqual(report['language_markers'], 625)

    def test_shape(self):
        text, entities = score.read(SHIPPED)
        self.assertEqual(len(entities), 624)
        self.assertEqual(len({e.entity_id for e in entities}), 624)
        self.assertTrue(text.startswith('<?xml version="1.0" ?>\r\n'))
        self.assertEqual(len(score.source_strings(entities)), 1126)
        for ent in entities:
            self.assertEqual(set(ent.fields), set(score.LOCALISED_FIELDS))
            self.assertEqual(len(ent.fields), 5)


if __name__ == '__main__':
    unittest.main()
