"""Sensitivity: would each detector have caught a defect we ACTUALLY fixed?

This is the only evidence that the detector set is any good. A detector that has
never fired proves nothing, and a clean report proves nothing either - the map
being clean and the detectors being blind look identical from the outside. So
every case below takes a defect that AGENT.md or a tool docstring records as
"found by hand in round N", puts the OLD value back into a copy of the map, runs
the detector that was later written to cover that class, and asserts it fires.

The point is not that the map is clean - `test_clean_map` covers that. The point
is that the cleanliness is earned rather than lucky.

Each case is (detector, key, old_value, round, where it was found). The old
values are transcribed from the docstrings of the tools that found them, which
is where the project already wrote them down.

  python tools/tests/run.py -v TestDetectors
"""
import copy
import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(HERE)
ROOT = os.path.dirname(TOOLS)
for p in (ROOT, TOOLS):
    if p not in sys.path:
        sys.path.insert(0, p)

import audit                                       # noqa: E402
import build                                       # noqa: E402
import dupes                                       # noqa: E402

VI = os.path.join(ROOT, 'translations', 'vi.json')

with open(VI, encoding='utf-8') as _h:
    REAL = json.load(_h)
SRC, LONGEST = audit._load_src()


def with_value(key, bad):
    """A copy of the map with one key put back to its pre-fix value."""
    m = copy.deepcopy(REAL)
    assert key in m, f'test names a key that does not exist: {key!r}'
    m[key] = bad
    return m


class TestDetectors(unittest.TestCase):
    """Every method is one historical defect, replayed."""

    def fires(self, detector, key, bad):
        m = with_value(key, bad)
        return audit.count_on(detector, m, SRC, LONGEST)

    def assertFires(self, detector, key, bad, round_no, why):
        before = audit.count_on(detector, REAL, SRC, LONGEST)
        after = self.fires(detector, key, bad)
        self.assertGreater(
            after, before,
            f'{detector} did NOT fire on the round-{round_no} {why}\n'
            f'     key {key!r}\n     old value {bad!r}\n'
            f'     count went {before} -> {after}')

    # -- round 60: the label and the value swapped halves -----------------
    def test_round60_misplaced_prefix(self):
        self.assertFires('prefix', 'CC: Attack Time', 'Thời gian CC: Attack',
                         60, 'misplaced "Word: " prefix')

    # -- round 61: two English words collapsed onto one phrase -------------
    def test_round61_collapsed_phrase(self):
        self.assertFires('collapsed', 'Flatten (with Options & Preferences)',
                         'Làm phẳng (với Tùy chọn & Tùy chọn)',
                         61, 'collapsed phrase')

    def test_round61_collapsed_phrase_english(self):
        """The reverse: the ENGLISH repeats, so it is a parallel construction
        and must NOT fire. A detector that fires on both directions is a
        detector that cries wolf, which AGENT.md §7 says is worse than none."""
        key = 'Flatten (with Options & Preferences)'
        src2 = dict(SRC)
        src2[key] = 'Bar and Bar'      # the English repeats one phrase on purpose
        before = audit.count_on('collapsed', REAL, SRC, LONGEST)
        after = audit.count_on('collapsed', with_value(key, 'Nhịp và Nhịp'),
                               src2, LONGEST)
        self.assertEqual(before, after,
                         'collapsed fired although the English also repeats')

    # -- round 59: an English past participle where the verb belongs -------
    def test_round59_past_participle(self):
        """Round 59's own example. It needs `funcwords 1`, not the default 2 -
        see TestKnownBlindSpots."""
        before = audit.count_on('funcwords', REAL, SRC, LONGEST, args=['1'])
        after = audit.count_on('funcwords', with_value('Used in Project: %s',
                                                       'Used trong Project: %s'),
                               SRC, LONGEST, args=['1'])
        self.assertGreater(after, before,
                           'funcwords 1 did not fire on the round-59 case')

    # -- round 33/34: the English sentence left standing -------------------
    def test_round34_notation_frame(self):
        key = ('Notes for Which Accidentals Have Already Been Stated Within '
               'the Bar')
        if key not in REAL:
            self.skipTest(f'key not in this build: {key!r}')
        self.assertFires('frame', key, key, 34, 'notation string left in English')

    # -- round 32/38/40/44: a clause with a condition or a cost dropped ---
    def test_round32_dropped_clause(self):
        key = ('Picks up on the value of the %s function as soon as the control '
               'reaches that value. This results in smooth value changes, but '
               'requires you to estimate the pickup value.')
        if key not in REAL:
            self.skipTest('key not in this build')
        self.assertFires('dropped', key,
                         'Chức năng %s nhận giá trị khi Control tới đúng giá trị '
                         'đó.', 32, 'second sentence dropped')

    def test_round44_dropped_clause(self):
        key = ('When bar numbers are positioned at barlines, you may prefer '
               'dynamics to be placed closer to the staff than bar numbers, or '
               'vice versa. This has no effect for bar numbers centered on the '
               'bar, which are always placed outside dynamics.')
        if key not in REAL:
            self.skipTest('key not in this build')
        self.assertFires('dropped', key,
                         'Khi số Bar đặt tại Barline, bạn có thể đặt Dynamics gần '
                         'Staff hơn số Bar hoặc ngược lại.',
                         44, 'second sentence dropped')

    # -- round 45/46/47: a quoted name that does not match its label ------
    def test_round45_quote_kept_english(self):
        key = "All parts specified in 'Part Editing Mode' are used."
        if key not in REAL:
            self.skipTest('key not in this build')
        # the label is "Chế độ Edit Part", so quoting the English is wrong
        self.assertFires('quotes', key, "All parts specified in 'Part Editing Mode' are used.",
                         45, 'quoted English where the label is Vietnamese')

    def test_round45_quote_matching_label_is_correct(self):
        """The other direction must NOT fire. Quoting the label's own
        translation is correct, and the first version of this tool asserted the
        opposite for eleven values."""
        key = "All parts specified in 'Part Editing Mode' are used."
        if key not in REAL:
            self.skipTest('key not in this build')
        before = audit.count_on('quotes', REAL, SRC, LONGEST)
        after = self.fires('quotes', key,
                           "Dùng tất cả Part đã chọn trong 'Chế độ Edit Part'.")
        self.assertEqual(before, after,
                         'quotes fired on a value that matches its label')

    # -- round 66: the extractor's disambiguation note in the text -------
    def test_round66_gloss_in_value(self):
        if 'Link [short, verb]' not in REAL:
            self.skipTest('key not in this build')
        m = copy.deepcopy(REAL)
        m['Link [short, verb]'] = 'Liên kết [ngắn, động từ]'
        # the map's own key is bare 'Link'; add the marked one explicitly
        src2 = dict(SRC)
        src2['Link [short, verb]'] = 'Link'
        long2 = dict(LONGEST)
        long2.setdefault('Link [short, verb]', []).append('Link [short, verb]')
        self.assertGreater(audit.count_on('gloss', m, src2, long2), 0,
                           'gloss did not fire on the round-66 marker')

    # -- round 40: a number dropped with the clause it belonged to --------
    def test_round40_dropped_number(self):
        """The dropped-clause class, and the one place a machine can see it.
        A number cannot survive a paraphrase by accident, so "44,1 kHz" going
        missing means the sentence it was in went missing with it."""
        key = ('Sample rate is not supported for video export. Set the audio '
               'sample rate to 44,1 kHz or 48 kHz.')
        if key not in REAL:
            self.skipTest('key not in this build')
        # the real value is CORRECT - it has the number. Drop it and the
        # detector must notice, which is what proves the detector is alive.
        self.assertFires(
            'numbers', key,
            'Sample Rate không hỗ trợ Export Video. Đặt Sample Rate Audio '
            'thành 48 kHz.',
            40, 'number dropped with its clause')

    def test_ordinal_is_not_a_missing_number(self):
        """1st -> Thứ nhất is CORRECT, and five of the first hits of the first
        version of this detector were 1st..5th. A detector that flags those is a
        detector nobody reads."""
        if '1st' not in REAL:
            self.skipTest('key not in this build')
        before = audit.count_on('numbers', REAL, SRC, LONGEST)
        after = audit.count_on('numbers', with_value('1st', 'Thứ nhất'),
                               SRC, LONGEST)
        self.assertEqual(before, after, 'numbers flagged an ordinal')

    def test_decimal_separator_is_not_a_missing_number(self):
        """Cubase writes a European decimal comma in its own English and
        Vietnamese writes a point. Comparing the text made this the only
        finding on the whole map, and our translation was the right one."""
        key = 'Sample rate is not supported for video export. Set the audio ' \
              'sample rate to 44,1 kHz or 48 kHz.'
        if key not in REAL:
            self.skipTest('key not in this build')
        before = audit.count_on('numbers', REAL, SRC, LONGEST)
        after = audit.count_on(
            'numbers',
            with_value(key, REAL[key].replace('44.1', '44,1')),
            SRC, LONGEST)
        self.assertEqual(before, after,
                         'numbers treated 44,1 and 44.1 as different numbers')

    # -- round 66: the [RM] marker belongs to the key, not the text -------
    def test_round66_rm_marker_in_value(self):
        self.assertTrue(
            build.check_value('Stacked[RM]', 'Xếp chồng[RM]', 'Stacked'),
            'style did not flag [RM] inside a value')
        self.assertFalse(
            build.check_value('Stacked[RM]', 'Xếp chồng', 'Stacked'),
            'style flagged a clean [RM] value')

    # -- round 72: `Bypass -> bỏ qua` is wrong; `Ignore -> bỏ qua` is not -
    def test_round72_bypass_is_conditional(self):
        self.assertTrue(build.check('Bypass this channel',
                                    'Bỏ qua Channel này'),
                        'style let Bypass -> bỏ qua through')
        self.assertFalse(build.check('Ignore this channel',
                                     'Bỏ qua mục này'),
                         'style blocked the correct Ignore -> bỏ qua')

    # -- round 174: `Suspend Read/Write` are Cubase's own names ------------
    def test_round174_suspend_read_write_stays_english(self):
        for term in ('Suspend Read', 'Suspend Write'):
            hits = build.check(f'{term} Automation',
                               f'Tạm dừng ghi {term}')
            self.assertFalse(hits, f'style forced {term!r} into Vietnamese')

    # -- round 189: two different instruments, one value ------------------
    def test_round189_temple_wood_block_collision(self):
        if 'Temple Block' not in REAL or 'Wood Block' not in REAL:
            self.skipTest('keys not in this build')
        import contextlib
        import io
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            groups = dupes.run_values()
        # the shipped map must NOT collide on these two
        self.assertGreaterEqual(len(groups), 0)
        for keys, _value in groups:
            self.assertNotEqual({'Temple Block', 'Wood Block'}, set(keys),
                                'Temple Block and Wood Block share a value again')

    # -- round 200: a STATUS sentence rendered as an IMPERATIVE -------------
    def test_round200_status_rendered_as_imperative(self):
        """I made this mistake myself, twice.

        round 196 changed 'All parts in editor are used.' - a line of status text
        in the Info Line - into 'Dung tat ca Part trong Editor.', which reads as an
        instruction. round 199 then found the sibling 'All clips in editor are
        used.', called it "perfectly symmetrical" and copied the defect into it.

        This is the test that had to exist before round 199, and did not.
        """
        self.assertFires('status', 'All clips in editor are used.',
                         'Dùng tất cả Clip trong Editor.',
                         200, 'status sentence turned into an imperative')

    def test_round200_shipped_family_is_consistent(self):
        """The whole 'are used' family must use the status form, and the
        shipped map already carries one correct sibling ('All audio files are
        used' -> 'Tat ca file Audio deu dang dung'). That sibling is the proof
        that the imperative reading is the wrong one - so when one string of a
        family is fixed, ask what the siblings say, not what looks natural.
        """
        family = ['All clips in editor are used.',
                  'All parts in editor are used.',
                  "All clips specified in 'Clip Editing Mode' are used.",
                  "All parts specified in 'Part Editing Mode' are used."]
        if not all(k in REAL for k in family):
            self.skipTest('keys not in this build')
        self.assertEqual(0, audit.count_on('status', REAL, SRC, LONGEST))
        # and the rule cuts the other way too: that same sibling, put back into
        # the imperative, IS a finding - so "đang dùng" is the required reading
        self.assertEqual(1, self.fires('status', 'All audio files are used',
                                       'Dùng tất cả file Audio.'))

    def test_round200_english_imperative_source_is_not_a_finding(self):
        """'Select which notes are used for ...' contains 'are used' but the
        English is an instruction too, so an imperative Vietnamese value is
        correct. Without this guard the detector reports 3 false positives on
        7 candidates and stops being read (AGENT.md §7).
        """
        before = audit.count_on('status', REAL, SRC, LONGEST)
        for key, bad in [
            ("Select which notes are used for 'Randomize', 'Create Variation' "
             "and 'Add Voice'", 'Chọn nốt nào dùng cho \'Ngẫu nhiên hóa\'.'),
            ('Use Drum Editor when Drum Map is assigned',
             'Dùng Drum Editor khi có Drum Map.'),
        ]:
            if key not in REAL:
                continue
            self.assertEqual(before, self.fires('status', key, bad),
                             f'status fired on an imperative source: {key!r}')


class TestKnownBlindSpots(unittest.TestCase):
    """What the set CANNOT see, asserted so it stays true.

    These are the honest answer to "is the detector set strong enough": two
    defect classes that this project has actually fixed before are, at default
    settings, invisible to every detector. Both were found by reading
    (AGENT.md §8.9: "lỗi chỉ lộ ra khi đọc thật") and the detector written for the
    class did not cover the case that was actually found.

    Asserting the blindness is deliberate. A detector that quietly misses a
    class is worse than one that is known to, because the report looks clean.
    If a test here starts FAILING, a rule has been added: move it up to
    TestDetectors as a positive case and note it in AGENT.md §7.

    round 33 - the English frame. `frame` needs a run of 4 English words that all
    appear in the source. The defective value is
    "Nhấp 'Bắt đầu' vao scan cho unreferenced files" and `cho` is NOT in the
    source ("to scan for unreferenced files"), so every 4-window is broken and
    the longest clean run is 2. `funcwords` also misses it - `cho` is one
    function word and the threshold is 2. `thin` catches it, and `thin` is a
    LEAD generator, not a defect detector.

    round 59 - the past participle, and WHY it was invisible. "Used trong
    Project: %s" contains exactly one English verbish token, so `funcwords`
    at its default threshold of 2 cannot see it, and at `funcwords 1` it fires
    with 63 candidates instead of 1. That is the trade AGENT.md §7 keeps
    making: precision first, because a detector that cries wolf is not read.

    The gate was the bigger problem and it is now gone. `funcwords` used to ask
    `HAN.search(v)` first, and `trong` is plain ASCII - so round 59's value has
    no non-ASCII character at all and the detector never looked at it. Round 193
    removed the gate and measured that it adds zero findings to the shipped map.
    """

    def assertBlind(self, detectors, key, bad, round_no, why):
        m = with_value(key, bad)
        for name, args in detectors:
            before = audit.count_on(name, REAL, SRC, LONGEST, args=args)
            after = audit.count_on(name, m, SRC, LONGEST, args=args)
            self.assertEqual(after, before,
                             f'{name}{args} now catches the round-{round_no} '
                             f'{why} - that is an improvement, so move this '
                             'case up into TestDetectors and say so in '
                             'AGENT.md section 7')

    def test_round33_frame_is_invisible(self):
        self.assertBlind(
            [('frame', []), ('funcwords', []), ('leftover', []),
             ('dropped', []), ('quotes', []), ('gloss', []), ('prefix', [])],
            "Click 'Start' to scan for unreferenced files",
            "Nhấp 'Bắt đầu' vao scan cho unreferenced files",
            33, 'English frame')

    def test_round59_participle_needs_threshold_one(self):
        """Visible only at `funcwords 1`. Kept as a blind spot because raising
        the default is a precision decision, not a bug fix."""
        self.assertBlind(
            [('funcwords', []), ('frame', []), ('opening', [])],
            'Used in Project: %s', 'Used trong Project: %s',
            59, 'past-participle frame')

    def test_the_accent_gate_was_the_round59_blind_spot(self):
        """It is gone now, so this asserts the FIXED state rather than the
        blindness: the bad value is pure ASCII and `funcwords 1` sees it. If a
        future edit puts an accent gate back, this is what fails."""
        m = with_value('Used in Project: %s', 'Used trong Project: %s')
        self.assertFalse(audit.HAN.search(m['Used in Project: %s']),
                         'the round-59 value is no longer pure ASCII - the '
                         'test case needs rewriting')
        self.assertGreater(
            audit.count_on('funcwords', m, SRC, LONGEST, args=['1']),
            audit.count_on('funcwords', REAL, SRC, LONGEST, args=['1']))

    def test_a_lead_generator_does_see_round33(self):
        """So the class is not entirely uncovered - just uncovered by anything
        that asserts a defect. Recorded here so nobody repeats the measurement."""
        m = with_value("Click 'Start' to scan for unreferenced files",
                       "Nhấp 'Bắt đầu' vao scan cho unreferenced files")
        self.assertGreater(audit.count_on('thin', m, SRC, LONGEST),
                           audit.count_on('thin', REAL, SRC, LONGEST))


class TestCleanMap(unittest.TestCase):
    """The map itself: what a clean run must look like. If these fail, a
    detector started crying wolf - which AGENT.md §7 calls worse than useless."""

    # Detectors that must find NOTHING in the shipped map. Each one found a real
    # defect at some point, so 0 here means the defects were fixed, not that the
    # detector is dead. `test_above` is what proves it is not dead.
    SILENT = ['leak', 'leftover', 'dropped', 'quotes', 'gloss', 'prefix',
              'funcwords', 'same_en', 'numbers']

    def test_silent_detectors_find_nothing(self):
        noisy = []
        for name in self.SILENT:
            n = audit.count_on(name, REAL, SRC, LONGEST)
            if n:
                noisy.append(f'{name}={n}')
        self.assertEqual(noisy, [],
                         'these should be 0 in the shipped map: ' + ', '.join(noisy))

    def test_audit_quality_glossary_is_known_not_broken(self):
        """AGENT.md has recorded `quality`'s glossary section as stale for
        several rounds. It is still counted, so record the number instead of
        pretending it is zero - a permanent false alarm that is written down is
        a known item; one that is hidden is a trap."""
        n = audit.count_on('quality', REAL, SRC, LONGEST)
        self.assertLessEqual(n, 12,
                             f'quality now reports {n}; the documented stale '
                             'glossary was 7, so something changed - read it')


if __name__ == '__main__':
    unittest.main(verbosity=2)