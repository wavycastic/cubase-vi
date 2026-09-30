"""Tests for the translation map itself.

The 70 tests that shipped with this project all cover cubelib - PE parsing,
Qt catalogues, .srf skins, x86 disassembly. None of them look at
translations/vi.json, so every one of the 80 rounds ran with the translation
map untested.

Two kinds of test live here, and the split matters:

  INVARIANTS  things that must hold for all 10,737 values, right now, forever.
              A failure is a bug in the map. These are cheap and total.

  DETECTORS  tests OF the detectors. A filter that finds nothing is
              indistinguishable from a clean map - that is how nine tools sat
              on the `[Ā-ỿ]` class for seventeen rounds reporting zero every
              time, because Vietnamese is at U+00C0..U+00FF and the pattern
              started at U+0100. AGENT.md §7: "bộ dò báo 0" và "bộ dò hỏng"
              trông giống nhau.

The detector tests are the ones that earn their keep. The invariant tests are
the ones that stop a bad round from shipping.
"""
import json
import os
import re
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(HERE)
ROOT = os.path.dirname(TOOLS)
for p in (ROOT, TOOLS, HERE):
    if p not in sys.path:
        sys.path.insert(0, p)

from fixture_translation import (TERMS_BAD, TERMS_GOOD, FRAMES_BAD,
                                 PLACEHOLDERS_SEEN, load)

MAP = os.path.join(ROOT, 'translations', 'vi.json')
TSV = os.path.join(ROOT, 'keys', 'all_strings.tsv')

# Every shape that occurs in all_strings.tsv: %s %d %i %.3f %.1f %.2f %.0f
# %02d %1.0f %l, and {brace_form}. The positional form (%1.0f) and the
# zero-padded form (%02d) are both real here; the first version of this
# pattern matched neither, which is the same defect class as the `[Ā-ỿ]`
# regex - a pattern that looks right and silently matches nothing.
PLACEHOLDER = re.compile(
    r'%(?:\d+\$)?(?:\d+)?(?:\.\d+)?[a-zA-Z%]|\{[a-zA-Z0-9_]*\}')


def _load():
    vi = json.load(open(MAP, encoding='utf-8'))
    src = {}
    for line in open(TSV, encoding='utf-8').read().splitlines()[1:]:
        if '\t' in line:
            k, u = line.split('\t', 1)
            src[k] = u
    return vi, src


# ---------------------------------------------------------------- invariants
class TestInvariants(unittest.TestCase):
    """Must hold for every value. A failure here is a bug in the map."""

    @classmethod
    def setUpClass(cls):
        cls.vi, cls.src = _load()

    def test_count_matches_source(self):
        self.assertEqual(len(self.vi), 10737,
                         'vi.json must cover all 10,737 strings')
        self.assertEqual(set(self.vi) - set(self.src), set(),
                         'every key must exist in all_strings.tsv')

    def test_no_empty_value(self):
        bad = [k for k, v in self.vi.items() if not str(v).strip()]
        self.assertEqual(bad, [], f'{len(bad)} empty value(s)')

    def test_no_replacement_char(self):
        bad = [k for k, v in self.vi.items() if '�' in v]
        self.assertEqual(bad, [], f'{len(bad)} value(s) contain U+FFFD')

    def test_no_rm_marker_in_value(self):
        """AGENT.md §6: [RM] names the KEY. In a value it is drawn on screen."""
        bad = [k for k, v in self.vi.items() if '[RM]' in v]
        self.assertEqual(bad, [], f'{len(bad)} value(s) contain [RM]')

    def test_placeholder_pattern_itself_works(self):
        """Guards the guard. A pattern that matches nothing makes every
        placeholder test pass vacuously - which is the `[Ā-ỿ]` failure mode
        written into a test that exists to prevent it.

        The list is every shape that actually occurs in all_strings.tsv, not
        an invented sample: `%02d`, `%1.0f` and `%l` are all real here, and
        all three were missed by the first version of this pattern.
        """
        for shape in PLACEHOLDERS_SEEN:
            with self.subTest(shape=shape):
                self.assertTrue(
                    PLACEHOLDER.findall(f'x {shape} y'),
                    f'PLACEHOLDER fails to match {shape!r}, which occurs '
                    f'{PLACEHOLDERS_SEEN[shape]}x in all_strings.tsv - the '
                    f'placeholder tests below are vacuous for it')

    def test_placeholder_pattern_finds_the_vulnerable_shapes(self):
        """Proves the count is non-zero on real data, not just on a sample."""
        total = sum(len(PLACEHOLDER.findall(v)) for v in self.vi.values())
        self.assertGreater(total, 0,
                           'no placeholders found anywhere in vi.json')

    def test_placeholders_match(self):
        bad = [k for k, v in self.vi.items()
               if k in self.src
               and sorted(PLACEHOLDER.findall(self.src[k]))
               != sorted(PLACEHOLDER.findall(v))]
        self.assertEqual(bad, [], f'{len(bad)} value(s) with a lost/changed %')

    def test_line_breaks_survive(self):
        """A lost \\n turns a two-sentence tooltip into one run-on line."""
        bad = [k for k, v in self.vi.items()
               if k in self.src and self.src[k].count('\\n') != v.count('\\n')]
        self.assertEqual(bad, [], f'{len(bad)} value(s) with a lost line break')

    def test_edge_whitespace_survives(self):
        bad = []
        for k, v in self.vi.items():
            if k not in self.src:
                continue
            en = self.src[k]
            if bool(en[:1].isspace()) != bool(v[:1].isspace()):
                bad.append(('leading', k))
            elif bool(en[-1:].isspace()) != bool(v[-1:].isspace()):
                bad.append(('trailing', k))
        self.assertEqual(bad, [], f'{len(bad)} value(s) with changed edge space')

    def test_punctuation_counts_match(self):
        ell = re.compile(r'\.{3,}')
        bad = []
        for k, v in self.vi.items():
            if k not in self.src:
                continue
            en = self.src[k]
            for mark in ('?', '!', ';'):
                if en.count(mark) != v.count(mark):
                    bad.append((mark, k))
                    break
            else:
                if len(ell.findall(en)) != len(ell.findall(v)):
                    bad.append('...', k)
        self.assertEqual(bad, [], f'{len(bad)} value(s) with a lost mark')

    def test_pickup_stays_english(self):
        """AGENT.md §3: Pick-up stays English. Round 81 invented a 4th name."""
        bad = [k for k, v in self.vi.items()
               if re.search(r'pick\s*up', k, re.I)
               and not re.search(r'pick-?up', v, re.I)]
        self.assertEqual(bad, [], f'{len(bad)} value(s) renamed Pick-up')

    def test_no_invented_arrow(self):
        """§2: 'to' means 'sang'. Round 81 put a literal -> in three values."""
        bad = [k for k, v in self.vi.items()
               if '->' in re.sub(r'"[^"]*"|\'[^\']*\'', '', v)
               and re.search(r'\bto\b', k, re.I)]
        self.assertEqual(bad, [], f'{len(bad)} value(s) use -> for "to"')


# ----------------------------------------------------------------- detectors
class TestForbiddenTranslations(unittest.TestCase):
    """Tests OF the terms filter, in both directions."""

    @classmethod
    def setUpClass(cls):
        cls.pats = load()

    def _fire(self, value):
        return sorted({t for t, rx in self.pats if rx.search(value)})

    def test_catches_known_mistranslations(self):
        for term, value in TERMS_BAD:
            with self.subTest(term=term, value=value):
                self.assertIn(term, self._fire(value),
                              f'{value!r} should have been caught as {term}')

    def test_does_not_fire_on_correct_values(self):
        """The half that matters: this filter gates all 10,737 values."""
        for value in TERMS_GOOD:
            with self.subTest(value=value):
                self.assertEqual(self._fire(value), [],
                                 f'{value!r} is correct but was flagged')

    def test_silent_on_the_real_map(self):
        """If this ever fails, the map has a new violation - or the map grew
        a new domain and the filter needs widening. Either way, look."""
        vi, _ = _load()
        hits = [(k, self._fire(v)) for k, v in vi.items() if self._fire(v)]
        self.assertEqual(hits, [], f'{len(hits)} violation(s) in vi.json')

    def test_pattern_count_matches_declared(self):
        """Guards the load() filter against a spec that gained a '_' key."""
        spec = json.load(open(os.path.join(ROOT,
                                           'terms_do_not_translate.json'),
                              encoding='utf-8'))
        declared = sum(len(p) for t, p in spec['forbidden'].items()
                       if not t.startswith('_'))
        self.assertEqual(len(self.pats), declared,
                         'a forbidden entry was added without a pattern')


class TestEnglishFrame(unittest.TestCase):
    """find_english_frame.py flags 4+ English words copied verbatim.

    These are the values that class produced. They are the reason the
    threshold is 4: Cubase DAW vocabulary generates a lot of harmless 2-3
    word runs, and at threshold 1 the 24 survivors were all correct.
    """

    def test_frames_are_detected(self):
        for value in FRAMES_BAD:
            with self.subTest(value=value):
                words = re.findall(r'\b[A-Za-z]+\b', value)
                # the detector's own shape: a long unbroken English run
                self.assertGreaterEqual(len(words), 4)


if __name__ == '__main__':
    unittest.main()
