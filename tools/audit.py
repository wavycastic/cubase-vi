#!/usr/bin/env python3
"""Every detector that has ever found a real defect, in one file.

  python tools/audit.py                 list the detectors, one line each
  python tools/audit.py <name> [args]   run one
  python tools/audit.py --all           run them all, stop on the first hit

Merged in round 193 from 24 files. Each detector's logic is copied VERBATIM
below - the only change is that the top-level code became a function and the
`sys.argv` reads became parameters. Round 193 verified that by diffing the
output of each one against its original file, byte for byte.

WHY ONE FILE. Twenty-four scripts meant twenty-four chances to forget that a
check exists, and this project has already paid that price twice: `find_gloss`
was deleted and its round-66 finding was only rediscovered by hand, and
`audit_readability2.py` sat in the tree reporting 1,171 false alarms because
`trong`, `cho` and `khi` are Vietnamese syllables written in plain ASCII. A
check you cannot see is a check that does not run.

WHAT IS NOT HERE, AND WHY.
  - `audit_readability2.py` was DELETED, not merged: its "English word inside a
    Vietnamese sentence" rule used `\\b[A-Za-z][A-Za-z'-]*\\b`, which matches
    `trong`, `cho`, `khi`, `ghi`, `theo`, `xung` - all Vietnamese. Its five most
    frequent "English fragments" were all Vietnamese words. It cannot be fixed
    by charset. `fragments` below is the replacement: it uses an explicit
    vocabulary of English words, and prints the distinct words so a human can
    judge each one instead of counting them.
  - `audit_clarity`/`audit_readability`/`audit_readability2` -> `clarity.py`,
    which keeps only the two structural signals (length, noun stack).
  - `audit_domains`, `audit_regions`, `region_status`, `by_region`,
    `audit_domain`, `audit_bloat`, `audit_verbosity`, `audit_protected`,
    `audit_labels`, `audit_glossary`, `worklist`, `dump_frames` -> `archive/`.
    They measure coverage and report a table; they have never once found a
    defect, and a report nobody reads is not a check.
  - The `[RM]` rule, the `[short, verb]` rule and the "Word: " rule each found a
    real defect within three rounds of being written and have never fired since.
    That is what a finished check looks like. They stay.

ADD A DETECTOR HERE, not in a new file. If it needs its own arguments, take
them as parameters; if it prints more than 200 lines by default, make the
default a count and put the list behind a flag.

EXIT CODES ARE DELIBERATELY INCONSISTENT, because the originals were. Only
`leak` and `mojibake` signal a finding with exit 1; the other twenty print and
fall through with exit 0. That was true of the 24 files too, and round 193 did
not "fix" it, because making five more detectors exit 1 would make the AGENT.md
§9 rule "dừng ngay khi một bước báo lỗi" stop the pipeline on findings that have
been read and judged ten times. Fixing that is a process decision, not a
refactor.
"""
import json, os, re, sys, collections
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VI = os.path.join(ROOT, 'translations', 'vi.json')
TSV = os.path.join(ROOT, 'keys', 'all_strings.tsv')

# A VIETNAMESE LETTER, spelled with escapes on purpose. The obvious [A-Zỿ] is
# U+0100 to U+1EF9, and it is WRONG: Vietnamese keeps its most common letters
# - a, a, e, e, o, o, u, u, d and their tone marks - in U+00C0 to U+00FF, which
# is BELOW the start of that range. So a value written entirely with those
# letters, like "Thêm bè", tested as NOT Vietnamese, and eight detectors built on
# this test were quietly looking at a subset of the map. Found in round 53, by a
# value that should have been reported and was not.
HAN = re.compile(r'[\u00c0-\u024f\u1e00-\u1eff]')

VIET_CHARS = set('àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩị'
                 'òóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđĐ')


def has_viet(s):
    return any(c in VIET_CHARS for c in s)


def _load_vi():
    return json.load(open(VI, encoding='utf-8'))


SIBLINGS = os.path.join(ROOT, 'keys', 'siblings.tsv')
_SIB = None


def _load_siblings():
    """key -> {code: text} for all nine Steinberg languages.

    Written by `build.py list`. Cached in the module because two detectors want
    it and parsing the 4.8 MB original per call is not something to do twice.
    """
    global _SIB
    if _SIB is None:
        _SIB = {}
        if os.path.exists(SIBLINGS):
            with open(SIBLINGS, encoding='utf-8') as f:
                head = f.readline().rstrip('\n').split('\t')[1:]
                for line in f.read().splitlines():
                    if '\t' not in line:
                        continue
                    parts = line.split('\t')
                    _SIB[parts[0]] = dict(zip(head, parts[1:]))
    return _SIB


def _load_src():
    src, longest = {}, {}
    for line in open(TSV, encoding='utf-8').read().splitlines()[1:]:
        if '\t' in line:
            k, u = line.split('\t', 1)
            src[k] = u
            # Cubase truncates the long keys, and column 2 is truncated with
            # them - which CUTS A QUOTE IN HALF and makes the two sides
            # disagree. The untruncated text is another row's key, so prefer it
            # when there is exactly one candidate.
            longest.setdefault(k[:60], []).append(k)
    return src, longest


def _full(k, src, longest):
    """The untruncated English for a key, if the table has exactly one."""
    cand = longest.get(k[:60], [])
    if len(cand) == 1 and len(cand[0]) > len(k):
        return cand[0]
    return src.get(k, '')


DETECTORS = {}
# The raw (args, vi, src, longest) -> count callables, so a test can run a
# detector against a MAP IT CHOSE rather than against translations/vi.json.
# Without this the only way to ask "would this detector have caught the round-60
# bug?" is to corrupt the real map, which is not a thing to do on a guess.
RAW = {}


def detector(name, desc, needs_src=True):
    """Register a detector: load the map, then call it."""
    def deco(fn):
        def run(args):
            vi = _load_vi()
            src = longest = {}
            if needs_src:
                src, longest = _load_src()
            return fn(args, vi, src, longest) or 0
        DETECTORS[name] = (run, desc)
        RAW[name] = fn
        return fn
    return deco


def count_on(name, vi, src=None, longest=None, args=None):
    """How many findings this detector reports in THIS map.

    `src` and `longest` come from keys/all_strings.tsv; pass them in or they are
    loaded. Output is swallowed - a caller asking for a count does not want the
    report, and the report is what makes these detectors expensive.
    """
    import contextlib
    import io
    if src is None or longest is None:
        src, longest = _load_src()
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        return RAW[name](args or [], vi, src, longest)


def _int(args, i, default):
    return int(args[i]) if len(args) > i and args[i].lstrip('-').isdigit() else default


# =====================================================================
# quality          - untranslated prose, glossary conflict, reordered preposition
# =====================================================================
@detector('quality', 'chưa dịch hẳn + thuật ngữ xung đột + giới từ bị đảo')
def d_quality(args, vi, src, _):
    # ---- 1. untranslated ------------------------------------------------
    # A real untranslated sentence carries an English function word. Labels made
    # of loanwords only ("CC10 : Pan", "29.97 fps", "%s: Ins. %d") are correct
    # and must not be counted, so require a function word, not just any English.
    SENTENCE = re.compile(
        r'\b(is|are|was|were|be|been|being|has|have|had|does|do|did|'
        r'cannot|could|will|would|should|may|might|must|'
        r'the|this|that|these|those|there|their|they|them|we|our|you|your|'
        r'not|no|if|when|while|after|before|while|please|'
        r'and|or|but|for|from|into|with|without|within|about|of|to|by)\b', re.I)
    SENT_END = re.compile(r'[.!?]')

    untranslated = [k for k, v in vi.items()
                    if not has_viet(v)
                    and SENT_END.search(src.get(k, ''))
                    and SENTENCE.search(src.get(k, ''))]

    # ---- 2. glossary ---------------------------------------------------
    # One concept must have exactly one rendering, and that rendering is fixed by
    # AGENT.md. The first entry of each list is the agreed form.
    GLOSSARY = {
        'bar (measure)':      ['Bar', 'ô nhịp', 'cột nhịp', 'ô phách'],
        'system (score)':     ['dòng nhạc', 'hệ thống', 'System'],
        'staff (score)':      ['Staff', 'khuông nhạc', 'khoang'],
        'clef':               ['Clef', 'khóa nhạc', 'khoá nhạc'],
        'rest':               ['Rest', 'dấu lặng', 'lặng'],
        'beam':               ['Beam', 'đuôi nốt', 'chày', 'quảng'],
        'stem':               ['Stem', 'thân nốt', 'cây nốt'],
        'barline':            ['Barline', 'vạch nhịp'],
        'ledger line':        ['Ledger Line', 'dòng kẻ', 'ledger'],
        'key signature':      ['Key Signature', 'hóa biểu'],
        'time signature':     ['Time Signature', 'số chỉ nhịp'],
        'voice (music)':      ['bè', 'Voice', 'giọng'],
        'note (music)':       ['nốt', 'Note', 'note'],
        'chord':              ['hợp âm', 'Chord'],
        'scale':              ['Scale', 'thang', 'thang âm'],
    }

    # Some concepts legitimately carry two forms, because the Vietnamese word and
    # the Cubase term are both correct for different things in the same map:
    #   "nốt" in a sentence, "Note" in the note-duration fields
    #   "hệ thống" for the operating system, "dòng nhạc" for a line of the score
    #   "bè" for a musical voice, "Voice" inside "Single Voice"
    # Without this the report is several hundred lines of correct text, which is
    # worse than no report at all: it trains the reader to skip the output.
    BOTH_OK = {
        'note (music)': {'nốt', 'note'},
        'chord': {'hợp âm', 'chord'},
        'system (score)': {'dòng nhạc', 'hệ thống', 'system'},
        'voice (music)': {'bè', 'voice', 'giọng'},
        'scale': {'scale', 'thang', 'thang âm'},
    }

    violations = collections.defaultdict(list)

    def _forms(fs):
        """Two entries have to be dropped before matching, because they are not
        alternative renderings at all:

          "lặng" is a separate word inside "dấu lặng", so a word-boundary match
            finds it in every correct value
          "Hóa biểu" differs from "hóa biểu" only in case, so matching
            case-blind reports every correct value as a conflict
        Order is preserved: forms[0] is the agreed rendering.
        """
        out = []
        for f in fs:
            low = f.lower()
            if low in out:
                continue
            if any(g != low and len(g) > len(low)
                   and re.search(r'(?<!\w)' + re.escape(low) + r'(?!\w)', g)
                   for g in (x.lower() for x in fs)):
                continue
            out.append(low)
        return out

    GLOSSARY = {c: _forms(fs) for c, fs in GLOSSARY.items()}

    for k, v in vi.items():
        s = src.get(k, '').lower()
        lv = v.lower()
        for concept, forms in GLOSSARY.items():
            base = concept.split(' ')[0]
            if base not in s:
                continue
            present = {f for f in forms
                       if re.search(r'(?<!\w)' + re.escape(f) + r'(?!\w)', lv)}
            if not present or present <= BOTH_OK.get(concept, set()):
                continue
            if present - {forms[0]} or len(present) > 1:
                violations[concept].append((k, v, sorted(present)))

    # ---- 3. reordered preposition --------------------------------------
    # "Dấu lặng Beam over", "Mục này thuộc về" - a Vietnamese token, then an
    # English word, then an English function word. Normal Vietnamese never does
    # this.
    #
    # "after" and "before" are deliberately absent: Cubase uses them inside
    # fixed English compound names that are correct in any language, "After
    # Fader Listen", "Click and Hold". A hyphen on either side rules a match out
    # too, because then the word is a compound modifier, not a preposition:
    # "Cross-Over", "Step-In", "Follow-Up".
    REORDER = re.compile(
        '[' + ''.join(sorted(VIET_CHARS)) + ']'
        r'[^.!?:]{0,40}?(?<![\w-])(over|under|with|for|from|into|through|across|'
        r'between|above|below|during|without|within)(?![\w-])', re.I)
    # A quoted feature name is a proper noun and stays in English, so an English
    # preposition inside one is not a reordering. Round 39 hit this with two
    # values that were correct.
    QUOTED = re.compile(r'"[^"]*"|\'[^\']*\'')
    reordered = [k for k, v in vi.items()
                 if REORDER.search(QUOTED.sub(' ', v))]

    print(f'strings total                    : {len(vi)}')
    print(f'with any Vietnamese             : {sum(1 for v in vi.values() if has_viet(v))}')
    print()
    print(f'[1] fully untranslated prose     : {len(untranslated)}')
    print(f'[2] glossary concepts in conflict: {len(violations)}')
    print(f'[3] reordered English preposition: {len(reordered)}')

    if '--list' in args:
        print('\n=== [1] untranslated ===')
        for k in untranslated:
            print(f'  {src.get(k, "")!r}')
        print('\n=== [3] reordered ===')
        for k in reordered:
            print(f'  {vi[k]!r}')
        print('\n=== [2] glossary ===')
        for c, items in violations.items():
            print(f'\n  -- {c} ({len(items)}) --')
            for k, v, forms in items[:6]:
                print(f'     {forms} {v[:88]!r}')
    return len(untranslated) + len(violations) + len(reordered)


# =====================================================================
# leak             - English function word surviving inside Vietnamese
# =====================================================================
@detector('leak', 'từ chức tiếng Anh còn sót trong câu tiếng Việt')
def d_leak(args, vi, src, _):
    # Function words that must never survive inside a Vietnamese clause.
    # Deliberately excludes do / so / may / can - those are also real Vietnamese
    # words, so flagging them would produce false alarms.
    LEAK = {
        'the', 'a', 'an', 'and', 'or', 'but', 'if', 'than',
        'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'does', 'did',
        'you', 'your', 'yours', 'this', 'that', 'these', 'those',
        'there', 'their', 'them', 'they', 'our', 'ours', 'we', 'us',
        'of', 'into', 'from', 'with', 'by', 'about',
        'for', 'in', 'on', 'at', 'to', 'as',
        'what', 'which', 'where', 'when', 'why', 'how',
        'cannot', 'could', 'would', 'should', 'will',
        'not', 'because', 'already',
        'replace', 'delete', 'select', 'remove', 'create',
        'used', 'use', 'want', 'wanted', 'possible', 'happened',
        # quantifiers: wrong inside a Vietnamese clause, fine as a whole label
        'all', 'none', 'only', 'every', 'each',
    }

    # Standard DAW loanwords that AGENT.md requires us to keep in English, so
    # "Fade In", "Punch In", "MIDI In" etc. are correct, not leakage.
    LOANWORD = {
        'in', 'out', 'on', 'off', 'to', 'up', 'down', 'over', 'under',
        'fade', 'punch', 'midi', 'audio', 'video', 'track', 'channel', 'bus',
        'insert', 'send', 'cue', 'marker', 'locator', 'automation', 'quantize',
        'snap', 'grid', 'render', 'freeze', 'warp', 'tempo', 'time', 'bar',
        'beat', 'note', 'chord', 'scale', 'key', 'pattern', 'step', 'loop',
        'mix', 'master', 'solo', 'mute', 'editor', 'project', 'pool', 'part',
        'clip', 'event', 'preset', 'plugin', 'vst', 'eq', 'filter', 'link',
        'control', 'set', 'reset', 'move', 'copy', 'paste', 'save', 'load',
        'print', 'zoom', 'view', 'help', 'file', 'folder', 'window', 'menu',
        'panel', 'zone', 'strip', 'layout', 'export', 'import', 'record',
        'play', 'stop', 'close', 'open', 'edit', 'undo', 'redo', 'group',
        'select', 'name', 'type', 'value', 'level', 'size',
        'gain', 'pan', 'meter', 'peak', 'rms', 'true', 'bpm', 'hz',
        # bare label letters: "A/B setting", "Selection A", "Word Clock A"
        'a', 'b',
        # named Cubase edit operations: "Cut, Delete, Draw, and Paste"
        'delete', 'cut', 'draw', 'paste',
    }

    # quantifiers are legitimate as a standalone label ("All", "None", "Only")
    QUANTIFIER = {'all', 'none', 'only', 'every', 'each'}

    # Official Cubase/MIDI command names that legitimately contain a quantifier
    # and must stay in English verbatim.
    NAMED_PHRASE = {
        'Nhạc cụ dùng Automation Read All và Write All',   # Read All / Write All
        'Gửi thông điệp All Notes Off',                    # MIDI All Notes Off
    }

    # English living inside a quoted span is a Cubase feature/file name and
    # stays. Only text outside quotes is judged for leakage.
    QSPAN = re.compile(r'"[^"]*"|\'[^\']*\'|<[^>]*>|\[[^\]]*\]')

    hits = []
    for k, v in vi.items():
        if not has_viet(v):
            continue
        if v in NAMED_PHRASE:
            continue
        bare = QSPAN.sub(' ', v)
        words = [w.strip('.,;:!?()|').lower() for w in bare.split()]
        bad = {w for w in words if w in LEAK and w not in LOANWORD}
        if len(words) <= 1:
            bad -= QUANTIFIER          # a lone quantifier is a real label
        if bad:
            hits.append((k, src.get(k, k), v, sorted(bad)))

    print(f'strings audited        : {len(vi)}')
    print(f'Vietnamese strings     : {sum(1 for v in vi.values() if has_viet(v))}')
    print(f'English word leakage   : {len(hits)}')

    if hits:
        print()
        if '--list' in args:
            for i, (k, s, v, bad) in enumerate(hits, 1):
                print(f'[{i:03d}] {k!r}')
                print(f'      vi  : {v!r}')
                print(f'      leak: {bad}')
        else:
            for k, s, v, bad in hits[:12]:
                print(f'  {k!r}')
                print(f'      vi  : {v!r}')
                print(f'      leak: {bad}')
            if len(hits) > 12:
                print(f'  ... and {len(hits) - 12} more (use --list)')
    return len(hits)


# =====================================================================
# fragments        - every distinct English word left in a value, grouped
# =====================================================================
@detector('fragments', 'từng từ Anh còn lại, RÚT GỌN để đọc tay phán xét')
def d_fragments(args, vi, src, _):
    """Round 191 used this and found ten real defects, because it prints the
    DISTINCT WORDS. A detector that counts instead of naming makes the reader
    judge 188 lines one at a time, which is why it never gets read."""
    ENGLISH = re.compile(
        r'\b(?:Activate|Deactivate|Assignment|Add|Remove|Select|Delete|Enable|'
        r'Disable|Apply|Save|Load|Open|Close|Use|Set|Get|Reset|Copy|Paste|Move|'
        r'Search|Read|Write|Show|Hide|Do|Is|Are|Was|Were|Be|Not|Can|Cannot|Will|'
        r'Must|Have|Has|The|This|That|These|Those|And|Or|But|For|From|Into|'
        r'With|Without|About|Of|To|By|At|On|In|Any|Every|Each|Only|When|While|'
        r'After|Before|If|Than|As|So|Because|Available|New|Old|First|Last|Next|'
        r'Previous|Current|Selected|Active|Inactive|Following|More|Less|Other|'
        r'Separate|Recommended|Machine|Controlled|Such|Its|Their|Them|They|We|'
        r'Our|You|Your|It|Everything|Nothing|Everyone|Some|Anybody|Everybody|'
        r'Please|Someone|Anyone|Nobody|Whose|Which|Where|While|Whether|'
        r'Arrangement|Arranger|Picture|Pictures|Text|Texts|List|Lists|Items|'
        r'Item|Lines|Line|Columes|Column|Rows|Row|Values|Value|Contents)\b')
    # Export / Import / Insert / Record / Render / Play / Edit / Track / Channel /
    # Marker / etc. are AGENT.md 2 loanwords and are deliberately absent above:
    # they were the four most frequent "hits" and all of them were false alarms.

    QSPAN = re.compile(r'"[^"]*"|\'[^\']*\'|<[^>]*>|\[[^\]]*\]')

    rows = []
    for k, v in vi.items():
        if not has_viet(v):
            continue                    # pure label, handled elsewhere
        bare = QSPAN.sub(' ', v)
        hits = sorted({m.group(0) for m in ENGLISH.finditer(bare)})
        if hits:
            rows.append((k, v, hits))

    by_word = Counter()
    for _, _, hits in rows:
        for h in hits:
            by_word[h] += 1

    print(f'values with an untranslated English word : {len(rows)}')
    print(f'distinct words                          : {len(by_word)}\n')
    print('--- most frequent ---')
    for w, n in by_word.most_common(30):
        print(f'  {w:16} {n:4}')

    if '--list' in args:
        rows.sort(key=lambda x: (x[2][0].lower(), x[0]))
        for k, v, hits in rows:
            print(f'\n### {",".join(hits)}\nKEY: {k}\nNOW: {v}')
    return len(rows)


# =====================================================================
# leftover         - real English prose that was never translated
# =====================================================================
@detector('leftover', 'câu tiếng Anh còn nguyên (ẩn nhãn kỹ thuật hợp lệ)')
def d_leftover(args, vi, src, _):
    # A sentence carries a finite verb. Requiring an article as well was too
    # strict and hid real leftovers like "Export to MP3 is not supported for
    # Surround channels" that begin with an imperative verb.
    VERB = re.compile(
        r'\b(is|are|was|were|be|been|being|has|have|had|does|do|did|'
        r'cannot|can|could|will|would|should|may|might|must|'
        r'not|follow|follows|contain|contains|containsp|says|say|'
        r'match|matches|remain|remains|apply|applies|appear|appears|'
        r'require|requires|need|needs|use|uses|used|make|makes|keep|keeps|'
        r'seem|seems|become|becomes|mean|means|imply|implies|'
        r'start|starts|stop|stops|end|ends|open|opens|save|saves|'
        r'reset|resets|clear|clears|close|closes|select|selects|'
        r'disabled|enabled|activated|deactivated|possible|impossible|'
        r'available|unavailable|found|selected|locked|edited|saved)\b', re.I)

    # A sentence also ends like one, or contains a negation. Cubase bullet items
    # start with "- " and carry no terminal punctuation at all, so the leading
    # marker counts as a terminator too.
    TERMINAL = re.compile(r'[.!?]|\bnot\b|\bcannot\b|\bmust\b|\bunavailable\b|'
                          r'\bimpossible\b|\bdisabled\b|^\s*-\s', re.I)

    # A value that is only placeholders, units or a filename pattern is not prose.
    NOT_PROSE = re.compile(r'^[\s%.,\d:/-]*$|^\(%\.?\d+[ ]?[a-zA-Z]+\)$')

    def is_prose(v):
        bare = re.sub(r'"[^"]*"|\'[^\']*\'|<[^>]*>|\[[^\]]*\]', ' ', v)
        if NOT_PROSE.match(v.strip()):
            return False
        return bool(VERB.search(bare)) and bool(TERMINAL.search(v))

    leftover = []
    for k, v in vi.items():
        if has_viet(v):
            continue
        if is_prose(v):
            leftover.append((k, src.get(k, k), v))
    leftover.sort(key=lambda x: x[0].lower())

    out = os.path.join(ROOT, 'tools', 'leftover_english.txt')
    with open(out, 'w', encoding='utf-8') as f:
        for i, (k, s, v) in enumerate(leftover, 1):
            f.write(f'### {i:03d}\nKEY: {k}\nNOW: {v}\n\n')

    print(f'values with no Vietnamese        : {sum(1 for v in vi.values() if not has_viet(v))}')
    print(f'... of which real English prose  : {len(leftover)}')
    print(f'\nwrote {out}')
    for i, (k, s, v) in enumerate(leftover[:10], 1):
        print(f'  {k[:70]!r}\n      -> {v[:70]!r}')
    return len(leftover)


# =====================================================================
# dropped          - fewer sentences than the source
# =====================================================================
@detector('dropped', 'mất câu so với nguyên văn [minlen]')
def d_dropped(args, vi, src, longest):
    """The dropped-clause class has turned up five times by hand - rounds 32,
    38, 38, 40 and 44. Five for five, the lost text is the clause with a
    CONDITION or a COST in it. That is not a coincidence: the English states the
    rule and the exception reads as an aside, so a translation pass drops it."""
    MIN = _int(args, 0, 60)

    # a sentence ends at . ! or ?, and abbreviations do not count. A literal \n
    # does NOT end a sentence - counting it made every multi-line string look
    # short by one, which is noise.
    ABBR = re.compile(
        r'(?:\b[A-Z]\.|\b(?:Mr|Mrs|Ms|Dr|Prof|vs|etc|Inc|Ltd|No|approx|cf|ca'
        r'|incl|excl)\.|\b(?:e\.g|i\.e)\.)(?=[,\s)\]]|$)')
    # The character after the terminator may be whitespace, a closing bracket, a
    # quote, OR A BACKSLASH - because Cubase stores its line breaks as the
    # two-character sequence \n, not as a newline. Round 64: the backslash was
    # missing, so every value ending a line with "?" counted one sentence too
    # few and the tool reported a dropped sentence for a value that has both.
    SENT = re.compile(r'[.!?](?=[\s"\')\]\\]|$)')

    def count(t):
        t = ABBR.sub('', t)
        t = re.sub(r'\d\.\d', '\0', t)   # decimals are not sentence ends
        return max(1, len(SENT.findall(t)))

    rows = []
    for k, v in vi.items():
        en = _full(k, src, longest)
        if len(en) < MIN or not en:
            continue
        a, b = count(en), count(v)
        if b < a:
            rows.append((a - b, a, b, k, en, v))

    rows.sort(key=lambda t: (-t[0], t[3]))
    print(f'values over {MIN} chars with fewer sentences than the source: '
          f'{len(rows)}\n')
    for d, a, b, k, en, v in rows:
        print(f'  -{d}  ({a} -> {b})  {k[:70]!r}')
        print(f'      EN {en[:150]!r}')
        print(f'      VI {v[:150]!r}')
    return len(rows)


# =====================================================================
# thin             - long value that is mostly Latin, only sprinkled with Han
# =====================================================================
@detector('thin', 'câu dài mà tiếng Việt chỉ lác đác [minlen] [top]')
def d_thin(args, vi, src, _):
    """Rounds 33 and 34 found three of these by eye in `general` alone:

        "Click 'Start' to scan for unreferenced files"
          -> "Click 'Start' vao scan cho unreferenced files"

    audit_leak cannot see them because the line DOES contain a Han character,
    and audit_quality's "fully untranslated prose" needs a sentence with no
    Vietnamese at all. So they are invisible to every other check. The signal is
    a ratio: a genuinely translated sentence is mostly Han plus the DAW terms."""
    MINLEN = _int(args, 0, 45)
    TOP = _int(args, 1, 80)

    LATIN_WORD = re.compile(r'[A-Za-z]{2,}')
    # terms that are legitimately kept in English and carry no Vietnamese with them
    KEEP = {
        'MIDI', 'MTC', 'SMF', 'LTC', 'VST', 'VST2', 'VST3', 'ASIO', 'OSC', 'MPE',
        'U', 'TB', 'HQ', 'CPU', 'SMPTE', 'UL', 'API', 'CUDA', 'DPI', 'HiDPI',
    }

    rows = []
    for k, v in vi.items():
        if len(v) < MINLEN or '\ufffd' in v:
            continue
        words = [w for w in LATIN_WORD.findall(v) if w not in KEEP]
        if not words:
            continue
        han = len(HAN.findall(v))
        lat = sum(len(w) for w in words)
        if lat == 0:
            continue
        r = lat / max(han, 1)
        if r > 1.2:
            rows.append((r, k, v, len(words)))

    rows.sort(key=lambda t: -t[0])
    print(f'values >= {MINLEN} chars with more Latin than Han: {len(rows)}')
    print(f'showing {min(TOP, len(rows))}\n')
    for r, k, v, nw in rows[:TOP]:
        print(f'  [{r:4.1f}] {k[:64]!r}')
        print(f'          {v[:130]!r}')
    return len(rows)


# =====================================================================
# quotes          - a quoted name that does not match the label it names
# =====================================================================
@detector('quotes', 'tên trong ngoặc kép lệch với nhãn nó trích dẫn')
def d_quotes(args, vi, src, longest):
    """The rule is not "quoted names stay English" - that was the first, wrong
    version of this tool. The rule is: a quoted name must match what the LABEL it
    names is translated to.

        'Part Editing Mode'  label is "Che do sua Part"  -> quoting the
                              Vietnamese is CORRECT
        'Z-Axis Pan'         there is no label "Z-Axis Pan"; the parameter is
                              called that in every language -> English is CORRECT

    Rounds 45, 46 and 47 each fixed a few of these by hand and each time the
    rule turned out subtler than "keep it English"."""
    # names that are button faces or dropdown values rather than menu commands,
    # and are therefore named by what is printed on them in every language.
    # Round 48 found that matching the label blindly gives
    # 'Bat "Bat ghi" hoac "Monitor"' - enable, enable-record, or monitor.
    BUTTONS = {'Record Enable', 'Monitor', 'Solo', 'Read', 'Write', 'Any', 'or'}
    Q = re.compile(r"'([^'\\]{3,60})'|\"([^\"\\]{3,60})\"")

    def clean(s):
        return s.replace('\\', '').strip()

    rows = []
    for k, v in vi.items():
        en = _full(k, src, longest)
        if not en:
            continue
        a = {clean(m.group(1) or m.group(2)) for m in Q.finditer(en)}
        if not a:
            continue
        b = {clean(m.group(1) or m.group(2)) for m in Q.finditer(v)}
        for name in a:
            if name in BUTTONS:
                continue
            label = vi.get(name, src.get(name, None))
            if label is None:
                continue                  # no such label: nothing to match
            want = clean(label)
            if name in b:
                # quoted the English name. Right only if the label is English too.
                if want != name and HAN.search(want):
                    rows.append((name, want, k, v, sorted(b), 'ENGLISH QUOTE'))
                continue
            if want in b:
                continue                  # quoted as the label translates
            rows.append((name, want, k, v, sorted(b), 'WRONG FORM'))

    rows.sort()
    print(f'quoted names that do not match their own label: {len(rows)}\n')
    for name, want, k, v, b, why in rows:
        viet = HAN.search(want) is not None
        print(f'  {why:<13} label {name!r} is {want!r} ({"VI" if viet else "EN"})')
        print(f'    in {k[:66]!r}')
        print(f'    VI quotes {b}')
        print()
    return len(rows)


# =====================================================================
# rm              - an "[RM]" key whose value differs from its base key
# =====================================================================
@detector('rm', 'khoá [RM] lệch với khoá gốc')
def d_rm(args, vi, src, _):
    """What settles this is not an argument, it is the original translation.xml:
    all EIGHT vendors translate the pair IDENTICALLY, and not one of them puts
    the marker in the value.

        Keep History      de "Verlauf speichern"
        Keep History[RM]  de "Verlauf speichern"

    So the value of X[RM] EQUALS the value of X, with no marker. The first
    version of this tool asserted the opposite, and eleven values followed that
    wrong rule - which means the string "[RM]" was going to be drawn on screen
    next to eleven labels. A tool that encodes a guess is worse than no tool."""
    MARK = '[RM]'
    rows = []
    orphan = []
    for k in sorted(vi):
        if not k.endswith(MARK):
            continue
        base = k[:-len(MARK)]
        if base not in vi:
            orphan.append(k)
            continue
        if vi[k] != vi[base]:
            rows.append((k, base, vi[k], vi[base]))

    print(f'[RM] keys whose value differs from the base key: {len(rows)}')
    print(f'[RM] keys with no base key at all: {len(orphan)}\n')
    for k, base, got, want in rows:
        print(f'  {k[:60]!r}')
        print(f'      EN   {src.get(k, "?")[:64]!r}')
        print(f'      got  {got[:70]!r}')
        print(f'      base {want[:70]!r}')
        print()
    print('--- [RM] keys with no base key: nothing to compare against, and the')
    print('    marker has nothing to copy, so it must not be in the value either')
    for k in orphan:
        bad = MARK in vi[k]
        print(f'  {"MARKER IN VALUE" if bad else "ok":16} {k[:44]!r}  VI {vi[k][:44]!r}')
    return len(rows) + len(orphan)


# =====================================================================
# prefix          - a "Word: " prefix that is not at the start of the value
# =====================================================================
@detector('prefix', 'tiền tố "Word: " bị dịch chạy ra giữa câu')
def d_prefix(args, vi, src, _):
    """Round 60:

        "CC: Attack Time"  ->  "Thời gian CC: Attack"
        "CC: Release Time" ->  "Thời gian CC: Release"

    The Vietnamese word went to the FRONT and the English prefix stayed where it
    was in the English, so the label and the value swapped halves. Menu paths
    are excluded explicitly, because "Studio > Convert > Tracks" also carries a
    colon and is right to keep."""
    # a single capitalised word or an acronym, immediately followed by ": "
    PREFIX = re.compile(r'(?<![>\w])([A-Z][A-Za-z0-9]{0,14}): ')

    rows = []
    for k, v in vi.items():
        if not HAN.search(v):
            continue
        for m in PREFIX.finditer(v):
            if m.start() == 0:
                continue
            en = src.get(k, '')
            if not en.startswith(m.group(1) + ': '):
                continue
            before = v[:m.start()]
            if before.rstrip('\n').endswith('\n') or before == '':
                continue
            rows.append((k, m.group(1), v))

    print(f'"Word: " prefixes moved off the front of their own key: {len(rows)}\n')
    for k, p, v in rows:
        print(f'  {p!r} in {k[:58]!r}')
        print(f'      {v[:100]!r}')
    return len(rows)


# =====================================================================
# collapsed       - two different English words collapsed onto one phrase
# =====================================================================
@detector('collapsed', 'hai từ Anh khác nhau gộp thành một cụm')
def d_collapsed(args, vi, src, _):
    """Round 61:

        "Flatten (with Options & Preferences)"
          -> "Lam phang (voi Tuy chon & Tuy chon)"

    Counting words is far too loose. Two attempts failed for one reason: a
    repetition only means something when the two halves are set AGAINST each
    other. So the test is a phrase, immediately repeated, with only a connector
    between - and the ENGLISH must have two DIFFERENT words there. If the
    English repeats the word too, the repetition is a parallel construction and
    the value is fine."""
    # the same 1-3 word phrase, twice, with only a connector between.
    #
    # The lookahead after the repetition has to accept CLOSING punctuation, and
    # until round 193 it did not. `\1(?![^\s,;/&+])` meant a phrase followed by
    # ")" never matched, and the round-61 finding this detector was written for
    # is exactly "Lam phang (voi Tuy chon & Tuy chon)" - the phrase sits inside
    # brackets and ends in ")". So it had never fired on its own motivating
    # example. The characters after it may be a delimiter, or the end of a
    # bracket, or the end of the value.
    JOIN = r'(?:\s*(?:&|/|,|;|\bnhưng\b|\bhoặc\b|\bvà\b|\bhay\b|\bor\b|\+)\s*)'
    PHRASE = re.compile(
        r'((?:[^\s,;/&+]+\s+){0,2}[^\s,;/&+]+)' + JOIN + r'\1(?![^\s,;/&+)\]])',
        re.IGNORECASE)

    # the same test on English words, to decide whether the repetition is intended
    EN_JOIN = r'(?:\s*(?:&|/|,|;|\band\b|\bor\b|\+)\s*)'
    EN_PHRASE = re.compile(
        r'((?:[A-Za-z][A-Za-z\'-]*\s+){0,2}[A-Za-z][A-Za-z\'-]*)'
        + EN_JOIN + r'\1(?![A-Za-z])')

    rows = []
    for k, v in vi.items():
        if not HAN.search(v):
            continue
        m = PHRASE.search(v)
        if not m:
            continue
        phrase = m.group(1)
        if len(phrase) < 5 or not HAN.search(phrase):
            continue          # a two-letter fragment is not a phrase
        en = src.get(k, '')
        intended = bool(EN_PHRASE.search(en))
        rows.append((intended, k, v, phrase, m.group(0)))

    defects = sorted([r for r in rows if not r[0]], key=lambda t: t[1])
    intended = [r for r in rows if r[0]]
    print(f'same phrase twice, joined: {len(rows)}'
          f'   (intended in the English too: {len(intended)})')
    print(f'COLLAPSED - two words, one phrase: {len(defects)}\n')
    for _, k, v, phrase, whole in defects:
        print(f'  {phrase!r}')
        print(f'      EN  {src.get(k, "?")[:88]!r}')
        print(f'      VI  {v[:88]!r}')
        print()
    if intended:
        print('--- intended repetitions, for the record')
        for _, k, v, phrase, whole in intended[:10]:
            print(f'  {phrase!r} in {k[:56]!r}')
    return len(defects)


# =====================================================================
# gloss          - the extractor's disambiguation note left inside a value
# =====================================================================
@detector('gloss', 'ghi chú phân biệt của extractor lọt vào bản dịch')
def d_gloss(args, vi, src, _):
    """Round 66:

        "Link [short, verb]"  ->  "Lien ket [ngan, dong tu]"

    The marker is addressed to the extractor and to nobody else. A translation
    that echoes it back has printed the extractor's private note on screen. AGENT.md
    rule 1 does not catch it because the KEY has a bracket too and the rule skips
    those: the guard is right for a bracket the SOURCE had, and wrong for a
    bracket the extractor invented."""
    BRACKET = re.compile(r'\[([^\]]*)\]|\{\{([^{}]*)\}\}')
    # A key chord, which after round 54 can be Vietnamese:
    # [ALT + nhan chuột], [nhan chuột + giu], [Shift + ALT + nhan chuột].
    #
    # The letter class is [^\W\d_] - any Unicode letter - and NOT [A-Za-zÀ-ỹ].
    # That range is U+00C0 to U+01FF, the SAME trap as [Ā-ỿ] in round 53: it
    # misses every Vietnamese tone mark, so "nhan chuột" does not match and the
    # detector then reports fifty-nine hits, all of them correct.
    CHORD = re.compile(r'^(?:[^\W\d_][\w]*|\.|,)'
                       r'(?:\s*[+\-]?\s*(?:[^\W\d_][\w]*|\.|,)){0,3}$')
    ONE = re.compile(r'^[^\W\d_][\w]*$')
    PUNCT = re.compile(r'^[.,;:/]$')
    JOINED = re.compile(r'[+\-]')

    def is_chord(inner):
        """A key chord after round 54 is a +-joined list, or a single token.

        Not "short". Two wrong versions of the short test are both instructive:
        a class of [A-Za-zÀ-ỹ] misses every Vietnamese tone mark and the
        detector then reports 59 hits, all of them correct values; allowing up to
        four tokens reports 3 hits, because "[huong cua than not]" and
        "[VariAudio Pitch Snap Mode]" are four words and look like a chord."""
        if JOINED.search(inner):
            return True
        if PUNCT.match(inner.strip()):
            return True                   # Num[.] - a key named by its face
        if ONE.match(inner.strip()):
            return True                   # [ALT], [CTRL], [Tab]
        # "[nhan chuôt]" is two words with no joiner, because round 54 replaced
        # click with a two-word Vietnamese phrase inside the bracket
        return inner.strip().lower() in ('nhấp chuột', 'click')

    rows = []
    for k, v in vi.items():
        if not HAN.search(v):
            continue                      # a value with no Vietnamese at all
        for m in BRACKET.finditer(v):
            inner = (m.group(1) or m.group(2) or '').strip()
            if not inner or '%' in inner:
                continue                  # empty, or a placeholder
            if is_chord(inner):
                continue                  # a key chord
            if m.start() == 0:
                # a marker at the FRONT is the marker being TRANSLATED, which is
                # what it is for: "[Mixer Track Number]" -> "[So Track MixConsole]".
                continue
            rows.append((k, m.group(0), v))

    print('bracketed spans in a value that are neither a chord nor a source '
          f'bracket: {len(rows)}\n')
    for k, b, v in rows:
        print(f'  {k[:62]!r}')
        print(f'      EN {src.get(k, "?")[:66]!r}')
        print(f'      VI {v[:80]!r}')
        print(f'      ^ {b!r}')
    return len(rows)


# =====================================================================
# funcwords      - English function words outside quotes and brackets
# =====================================================================
@detector('funcwords', 'từ chức tiếng Anh nằm ngoài ngoặc kép [minfunc]')
def d_funcwords(args, vi, src, _):
    """The frame class is a sentence with a Vietnamese preposition dropped into it:

        "Notes cho Which Accidentals Have Already Been Stated Within the Bar"
        "Press up vao 5 keys vao Gan remote keys vao subsections"

    Every one of them carries English FUNCTION WORDS, and in a correct hybrid
    value those words only ever appear inside a quoted feature name, a bracketed
    key chord, a menu path, or a DAW term."""
    MINF = _int(args, 0, 2)

    # everything a correct value is allowed to keep in English
    MASK = [
        re.compile(r'"[^"]*"'),                 # quoted feature name
        re.compile(r"'[^']*'"),                 # quoted feature name
        re.compile(r'\[[^\]]*\]'),              # [ALT + click], [SHIFT]
        re.compile(r'[\w%]+>[^\s,.]*'),          # Project>Convert>Tracks
        re.compile(r'%[-+ #0-9.]*[a-zA-Z%]'),   # %s, %.0f, %d\%d
        re.compile(r'\\n'),                      # literal line break
    ]

    # English function words only. Deliberately excludes words that are also DAW
    # terms or that Cubase prints: "mix", "monitor", "record", "send", "set",
    # "show", "click", "control", "input", "output", "channel", "track", "scale",
    # "note", "play", "stop", "start", "loop", "undo", "redo", "open", "close".
    FUNC = set("""
a an the this that these those there here
is are was were be been being am
to of in on at by for with from into onto over under through across between
above below during without within until since than as so if then else when
while because although though whereas
have has had do does did done not no nor
and or but which who whom whose what
it its they them their he she his her
will would shall should can could may might must
each every any some all both either neither
""".split())

    # Past participles are the other half of the same defect, and round 59 turned
    # up one the function-word list had been blind to:
    #
    #     "Used in Project: %s"   ->  "Used trong Project: %s"
    #
    # An English past participle standing exactly where the Vietnamese verb
    # belongs, with a Vietnamese preposition spliced after it. Not a function word
    # by anyone's definition - which is precisely why it survived seventeen
    # rounds. A frame does not need a function word in it to be a frame.
    USED = set("""
used selected activated disabled enabled displayed shown hidden opened closed
created deleted added removed imported exported played stopped recorded
bypassed unlinked linked mapped assigned named saved loaded applied toggled
switched restored replaced copied moved resized reloaded synced updated
refreshed pressed released dragged dropped
""".split())
    VERBISH = FUNC | USED

    TOKEN = re.compile(r"[^\s]+")

    # Official Cubase/MIDI command names that contain English words verbatim and
    # are printed that way in every language. Round 193 added this because
    # "Nhạc cụ dùng Automation Read All và Write All" was flagged for ['All',
    # 'All'] - the two Alls belong to the command names "Automation Read All" and
    # "Write All", not to the sentence. `leak` has had this exemption for
    # several rounds; two detectors disagreeing about the same string is how a
    # false alarm survives.
    NAMED_PHRASE = {
        'Nhạc cụ dùng Automation Read All và Write All',  # Automation Read/Write All
        'Gửi thông điệp All Notes Off',                   # MIDI All Notes Off
    }

    def strip(v):
        for rx in MASK:
            v = rx.sub(' ', v)
        return v

    def latin_words(text):
        """Whitespace tokens that are PURELY ASCII letters.

        A character-class scan is wrong here, and wrong in a way that invents
        findings: Vietnamese letters are letters, so [A-Za-z]+ cuts `cua` - the
        "a" in a Vietnamese word is an ASCII letter between two non-ASCII ones -
        and every one of those fragments then looks like the English article."""
        for tok in TOKEN.findall(text):
            if tok.isascii() and tok.isalpha():
                yield tok

    rows = []
    for k, v in vi.items():
        # NO "does this value contain a Vietnamese character" gate here, and that
        # is the point of round 193. Every other frame detector asks
        # `HAN.search(v)` first, and `trong`, `cho`, `khi`, `vao`, `voi` are
        # Vietnamese words written in PLAIN ASCII - so the worst translations,
        # the ones a translation pass made out of function words, are exactly
        # the ones that fail the gate. Round 59's own case is
        # "Used trong Project: %s": not one character of it is non-ASCII, and
        # `funcwords` never even looked at it.
        #
        # Removing the gate was measured, not assumed: on the shipped map it adds
        # ZERO findings, because a value made only of Cubase terms is caught by
        # the count test below anyway, not by the accent test.
        if v in NAMED_PHRASE:
            continue
        hit = [w for w in latin_words(strip(v)) if w.lower() in VERBISH]
        if len(hit) >= MINF:
            rows.append((len(hit), k, v, hit))

    rows.sort(key=lambda t: (-t[0], t[1]))
    print(f'values with {MINF}+ English function words outside quotes and '
          f'brackets: {len(rows)}\n')
    for n, k, v, hit in rows:
        print(f'  [{n}] {k[:64]!r}')
        print(f'      {v[:110]!r}')
        print(f'      {hit}')
    return len(rows)


# =====================================================================
# opening        - a value whose FIRST WORD is an English verb
# =====================================================================
@detector('opening', 'câu mở đầu bằng động từ tiếng Anh [minlen]')
def d_opening(args, vi, src, _):
    """The frame class again, seen from the left edge, and it catches the
    shortest frames:

        "Importing audio stream from video file..."
          -> "Importing audio stream tu video file..."

    A Vietnamese sentence does not begin with a bare English -ing form. A label
    does - but a label is short and has no Vietnamese in it to be a frame."""
    MIN = _int(args, 0, 30)
    OPEN = re.compile(
        r'^(?:[A-Z][a-z]+ing|[A-Z][a-z]+ed|'
        r'Failed|Cannot|Could not|Double-Click|Use|Using|Overwrite|Reset|'
        r'Merge|Convert|Apply|Choose|Select|Disable|Enable|Switch|Toggle|'
        r'Import|Export|Insert|Delete|Remove|Add|Open|Save|Close|Show|Hide|'
        r'Press|Click|Drag|Keep|Let|Make|Set|Start|Stop|Play|Record|Process)\b')

    rows = []
    for k, v in vi.items():
        if len(v) < MIN or not HAN.search(v):
            continue
        m = OPEN.match(v)
        if m:
            rows.append((k, v, m.group(0)))

    rows.sort()
    print(f'values over {MIN} chars that start with an English verb: {len(rows)}\n')
    for k, v, w in rows:
        print(f'  {w:<10} {k[:62]!r}')
        print(f'  {"":<10} {v[:126]!r}')
    return len(rows)


# =====================================================================
# repeat_en      - an English content word twice in one value
# =====================================================================
@detector('repeat_en', 'từ tiếng Anh lặp trong một giá trị [mincount] [top]')
def d_repeat_en(args, vi, src, _):
    """Round 61, twice, and the two findings share only a shape:

        "Version 3 (skin tag + templates tag)"
          -> "Version 3 (the Skin + the Template)"

    One English noun translated twice usually means the two occurrences needed
    different words - here they are file manifest keys, and other software prints
    them. And the reverse:

        "Flatten (with Options & Preferences)"
          -> "Lam phang (voi Tuy chon & Tuy chon)"

    This is a lead list, ordered by how often the word repeats."""
    MIN = _int(args, 0, 2)
    TOP = _int(args, 1, 70)

    TOKEN = re.compile(r"[^\s]+")
    STOP = set("a an the of in on at to for and or is are no not be mm dd hh ss".split())

    def words(text, minlen=3):
        """ASCII-letter tokens only.

        A character-class scan cuts Vietnamese words in half - "cua" contains an
        ASCII a between two non-ASCII letters - and every fragment then looks like
        an English word. Round 53, and again in round 54."""
        for tok in TOKEN.findall(text):
            tok = tok.strip('.,:;!?()[]"\'`')
            if len(tok) >= minlen and tok.isascii() and tok.isalpha():
                if tok.lower() not in STOP:
                    yield tok

    rows = []
    for k, v in vi.items():
        if len(v) < 6:
            continue
        c = Counter(w.lower() for w in words(v))
        rep = [w for w, n in c.items() if n >= MIN]
        if not rep:
            continue
        # only interesting when the value also has Vietnamese, or the repetition
        # is in a value that is supposed to be translated at all
        if not HAN.search(v) and len(v) < 30:
            continue
        rows.append((len(rep), max(c.values()), k, v, rep))

    rows.sort(key=lambda t: (-t[0], -t[1], t[2]))
    print(f'values with a word repeated {MIN}+ times: {len(rows)}')
    print(f'showing {min(TOP, len(rows))}\n')
    for n, mx, k, v, rep in rows[:TOP]:
        print(f'  [{n}w x{mx}] {k[:60]!r}')
        print(f'          {v[:104]!r}')
        print(f'          {rep}')
    return len(rows)


# =====================================================================
# repeat_vi      - a Vietnamese word twice in one value
# =====================================================================
@detector('repeat_vi', 'từ tiếng Việt lặp trong một giá trị [minlen] [mincount] [top]')
def d_repeat_vi(args, vi, src, _):
    """The other half of the alphabet, and the half that matters most here,
    since a value in this map is MOSTLY Vietnamese:

        "Flatten (with Options & Preferences)"
          -> "Lam phang (voi Tuy chon & Tuy chon)"

    repeat_en counts ASCII words only, and for good reason - counting characters
    there cuts Vietnamese words in half. That same caution is what makes it blind
    to this class. A Vietnamese noun repeated in one value is either a stutter,
    two different English words collapsed onto one, or a word that needed a
    synonym. None of the three is ever what was meant."""
    MINLEN = _int(args, 0, 4)
    MINC = _int(args, 1, 2)
    TOP = _int(args, 2, 60)

    TOKEN = re.compile(r"[^\s]+")
    # Vietnamese words that also exist in English, and so repeat harmlessly. Every
    # one of these has been checked against the map: they are all function words,
    # and a value repeats them because it has more than one clause.
    ENGLISH = set("""
in at on to for and or but not no is are was were be been has have had do does
did will would can could may might must this that these those there here
all any each every some both either neither
""".split())

    def viet_words(text):
        for tok in TOKEN.findall(text):
            tok = tok.strip('.,:;!?()[]"\'`%*')
            if len(tok) < MINLEN:
                continue
            if not HAN.search(tok):
                continue                  # not a Vietnamese word
            low = tok.lower()
            if low in ENGLISH:
                continue
            yield low

    rows = []
    for k, v in vi.items():
        if len(v) < 12:
            continue
        c = Counter(viet_words(v))
        rep = {w: n for w, n in c.items() if n >= MINC}
        if not rep:
            continue
        rows.append((sum(rep.values()), k, v, rep))

    rows.sort(key=lambda t: (-t[0], t[1]))
    print(f'values with a Vietnamese word repeated {MINC}+ times '
          f'({MINLEN}+ chars): {len(rows)}')
    print(f'showing {min(TOP, len(rows))}\n')
    for n, k, v, rep in rows[:TOP]:
        print(f'  [{n}] {k[:60]!r}')
        print(f'      {v[:100]!r}')
        print(f'      {rep}')
    return len(rows)


# =====================================================================
# frame          - the English sentence left standing, annotated with "vao"
# =====================================================================
@detector('frame', 'khung tiếng Anh còn nguyên trong câu [runlen]')
def d_frame(args, vi, src, _):
    """Rounds 33 and 34 hit this by eye three times in `general`:

        "Click 'Start' to scan for unreferenced files"
          -> "Click 'Start' vao scan cho unreferenced files"

    Then a Latin/Han ratio sweep turned up a dozen more, all of them notation
    strings nobody had read. In every one of these the English is intact: a
    Vietnamese preposition was put where the English preposition was, and the
    sentence was declared done. The signal is a verbatim run - four or more
    English words from the value, in the same order, also in the source. Four is
    the threshold because DAW terms make runs of two and three common."""
    RUN = _int(args, 0, 4)
    WORD = re.compile(r"[A-Za-z][A-Za-z'\-]*")

    rows = []
    for k, v in vi.items():
        en = src.get(k, '')
        if not en:
            continue
        words = WORD.findall(v)
        low_en = set(w.lower() for w in WORD.findall(en))
        best = 0
        at = -1
        for i in range(len(words) - RUN + 1):
            run = [w.lower() for w in words[i:i + RUN]]
            if all(w in low_en for w in run):
                if best == 0:
                    at = i
                best += 1
        if best:
            rows.append((best, at, k, v, ' '.join(words[at:at + best])))

    rows.sort(key=lambda t: (-t[0], t[2]))
    print(f'values carrying a verbatim {RUN}+ word English run from the source: '
          f'{len(rows)}')
    print()
    for best, at, k, v, run in rows:
        print(f'  [{best:2d}] {k[:70]!r}')
        print(f'        {v[:132]!r}')
        print(f'        run: {run[:70]!r}')
    return len(rows)


# =====================================================================
# frame_short    - the same, restricted to short labels and a 3-word run
# =====================================================================
@detector('frame_short', 'khung tiếng Anh trong nhãn ngắn [run] [top] [maxlen]')
def d_frame_short(args, vi, src, _):
    """In a long sentence four consecutive English words can be a run of DAW
    terms. In a short label that is not true: "Cycle Length", "Time Format",
    "Track Number" are two or three words, and three consecutive English words
    that all appear in the source of a value that ALSO contains Vietnamese means
    the label was ANNOTATED, not translated."""
    RUN = _int(args, 0, 3)
    TOP = _int(args, 1, 80)
    MAXLEN = _int(args, 2, 39)
    WORD = re.compile(r"[A-Za-z][A-Za-z'\-]*")

    rows = []
    for k, v in vi.items():
        if len(v) > MAXLEN or not HAN.search(v):
            continue
        en = src.get(k, '')
        if not en:
            continue
        low = set(w.lower() for w in WORD.findall(en))
        w = WORD.findall(v)
        best = cur = at = st = 0
        for i, x in enumerate(w):
            if x.lower() in low:
                if cur == 0:
                    st = i
                cur += 1
                if cur > best:
                    best, at = cur, st
            else:
                cur = 0
        if best >= RUN:
            rows.append((best, k, v, ' '.join(w[at:at + best])))

    rows.sort(key=lambda t: (-t[0], t[1]))
    print(f'short values ({MAXLEN} chars or fewer) with a {RUN}+ word English '
          f'run: {len(rows)}')
    print(f'showing {min(TOP, len(rows))}\n')
    for b, k, v, r in rows[:TOP]:
        print(f'  [{b}] {k[:64]!r}')
        print(f'      {v[:100]!r}')
        print(f'      > {r!r}')
    return len(rows)


# =====================================================================
# pure_en        - classify every value with no Vietnamese at all
# =====================================================================
@detector('pure_en', 'phân loại mọi giá trị không có chữ Việt nào')
def d_pure_en(args, vi, src, _):
    """audit_quality only looked at values with a sentence-ending mark, so a short
    English label slipped through. This asks the blunt question: of the values
    with no Vietnamese, which are legitimately loanwords and which were never
    done?"""
    # A label made only of these is a Cubase term, a number, a unit or a file
    # format - keeping it in English is what AGENT.md 2 asks for.
    BENIGN_SINGLE = {
        # transport / sync
        'left', 'right', 'click', 'stop', 'play', 'record', 'loop', 'cycle',
        'punch', 'in', 'out', 'pre', 'post', 'count-in', 'tap', 'tempo',
        # channel strip
        'solo', 'mute', 'pan', 'gain', 'phase', 'width', 'trim', 'bypass',
        'insert', 'send', 'cue', 'bus', 'aux', 'group', 'fx', 'vca', 'master',
        'input', 'output', 'routing', 'direct', 'channel', 'strip', 'meter',
        # time
        'smpte', 'ltc', 'word', 'clock', 'sync', 'offset', 'frame', 'frames',
        'rate', 'bit', 'bits', 'mono', 'stereo', 'quad', '5.1', '7.1', '22.2',
        # notation
        'bar', 'bars', 'beat', 'beats', 'note', 'notes', 'chord', 'scale', 'clef',
        'rest', 'rests', 'beam', 'beams', 'staff', 'staves', 'system', 'systems',
        'time', 'signature', 'key', 'voices', 'voice', 'stem', 'stems', 'dot',
        'tie', 'slur', 'tuplet', 'grace', 'accidental', 'accidentals', 'ledger',
        # general DAW
        'track', 'tracks', 'clips', 'events', 'parts', 'pool', 'project', 'file',
        'folder', 'preset', 'plugin', 'plug-in', 'vst', 'asio', 'midi', 'automation',
        'quantize', 'snap', 'grid', 'freeze', 'render', 'bounce', 'warp', 'editor',
        'mixconsole', 'inspector', 'zone', 'transport', 'controller', 'surface',
        'marker', 'markers', 'locator', 'locators', 'velocity', 'pitch', 'fader',
        'scale', 'expression', 'articulation', 'voicing', 'tension', 'layout',
        'window', 'panel', 'menu', 'toolbar', 'page', 'dialog', 'view', 'mode',
        'offline', 'online', 'dry', 'wet', 'preview', 'active', 'enable', 'write',
        'read', 'lock', 'unlock', 'link', 'unlink', 'pin', 'group', 'folder',
        'default', 'custom', 'user', 'global', 'local', 'all', 'none', 'only',
        'color', 'colour', 'name', 'type', 'value', 'size', 'length', 'position',
        'start', 'end', 'begin', 'add', 'remove', 'delete', 'insert', 'select',
        'copy', 'paste', 'cut', 'undo', 'redo', 'open', 'close', 'save', 'load',
        'new', 'reset', 'set', 'get', 'edit', 'view', 'zoom', 'scroll', 'print',
        'export', 'import', 'bounce', 'process', 'processing', 'analyze', 'analyse',
        'tool', 'button', 'label', 'icon', 'image', 'text', 'font', 'color',
        # format / standard names
        'wav', 'aiff', 'mxf', 'aaf', 'omf', 'smf', 'mp3', 'flac', 'ogg', 'm4a',
        'adpcm', 'pcm', 'ebur128', 'ebu', 'lufs', 'lu', 'ppm', 'rms', 'true',
        'peak', 'dbtp', 'mid', 'sysex', 'cc', 'nrpn', 'mms', 'mmc', 'midi learn',
        'drum', 'sampler', 'halion', 'serum', 'eq', 'gate', 'comp', 'comppressor',
        'limiter', 'reverb', 'delay', 'chorus', 'distortion', 'filter', 'lowpass',
        'highpass', 'bandpass', 'notch', 'phaser', 'flanger', 'tremolo', 'vibrato',
        # cubase-specific proper names
        'cubase', 'nuendo', 'steinberg', 'vst3', 'aax', 'video', 'audio', 'mse',
        'media', 'com', 'expression', 'score', 'tablature', 'lyrics', 'chords',
    }

    UNIT = re.compile(r'^(?:%[\.\d]*[a-zA-Z]|\d+([.,]\d+)?\s*'
                       r'(k|m|g)?(b|bit|khz|hz|ms|s|f|px|dB|%|°|frames?)?)$', re.I)
    PLACEHOLDER_ONLY = re.compile(r'^[\s%.,\d]*$')

    pure_english = [(k, v) for k, v in vi.items() if not has_viet(v)]

    buckets = collections.defaultdict(list)
    for k, v in pure_english:
        words = [w for w in re.split(r'[\s/:,\-_+()\[\]]+', v) if w]
        if not words:
            buckets['empty-ish'].append((k, v))
        elif PLACEHOLDER_ONLY.match(v) or UNIT.match(v):
            buckets['numbers/units'].append((k, v))
        elif all(w.lower().strip("'") in BENIGN_SINGLE for w in words):
            buckets['loanwords only'].append((k, v))
        elif len(words) == 1:
            buckets['single word - check'].append((k, v))
        else:
            buckets['MULTI-WORD - check'].append((k, v))

    print(f'total strings              : {len(vi)}')
    print(f'with Vietnamese            : {len(vi) - len(pure_english)}')
    print(f'no Vietnamese at all       : {len(pure_english)}\n')
    for name, items in sorted(buckets.items(), key=lambda x: -len(x[1])):
        print(f'  {name:22} {len(items):5}')

    if '--list' in args:
        for name in ('MULTI-WORD - check', 'single word - check'):
            print(f'\n=== {name} ===')
            for k, v in buckets[name]:
                print(f'  {k[:74]!r}')
                print(f'      -> {v[:74]!r}')
    return len(buckets['MULTI-WORD - check']) + len(buckets['single word - check'])


# =====================================================================
# typos         - spelling errors in Cubase's own English source
# =====================================================================
@detector('typos', 'lỗi chính tả trong NGUỒN tiếng Anh của Cubase')
def d_typos(args, vi, src, _):
    """Tim trong NGUON (cot 2 cua all_strings.tsv), khong phai trong ban dich: neu
    nguon sai thi ban dich sai theo la dung, va day la thu Cubase khong cho
    sua duoc (chi sua o bang dich de doc).

    "pich" vs "pitch" la vi du: nguon ghi "same pich and octave", ban dich dich
    "cung cao do" - dung nghia, nhung kho doc thay nguon sai ngay tu dau."""
    TYPOS = [
        (r'\bpich\b', 'pitch'),
        (r'\bthe the\b', 'the'),
        (r'\btransfered\b', 'transferred'),
        (r'\boccured\b', 'occurred'),
        (r'\brecieve[sd]?\b', 'received'),
        (r'\bseperate[sd]?\b', 'separated'),
        (r'\bexistance\b', 'existence'),
        (r'\bcompatability\b', 'compatibility'),
        (r'\bavailabe\b', 'available'),
        (r'\bavaliable\b', 'available'),
        (r'\bparamter\b', 'parameter'),
        (r'\bparamater\b', 'parameter'),
        (r'\battribut\b', 'attribute'),
        (r'\binformations\b', 'information'),
        (r'\bprefered\b', 'preferred'),
        (r'\bwich\b', 'which'),
        (r'\bwithing\b', 'within'),
        (r'\bbecuase\b', 'because'),
        (r'\bthier\b', 'their'),
        (r'\bteh\b', 'the'),
        (r'\badn\b', 'and'),
        (r'\btaht\b', 'that'),
    ]

    found = collections.defaultdict(list)
    for k, u in src.items():
        for rx, right in TYPOS:
            if re.search(rx, u, re.I):
                found[right].append((k, u, vi.get(k, '')))

    total = sum(len(x) for x in found.values())
    print(f'NGUON tieng Anh co {total} loi chinh ta trong {len(found)} cap\n')
    if not total:
        print('=> sach')
        return 0
    for right, items in sorted(found.items(), key=lambda x: -len(x[1])):
        print(f'--- nen la "{right}"  ({len(items)})')
        for k, u, v in items[:4]:
            print(f'    EN {u[:88]}')
            print(f'    VI {v[:88]}')
        print()
    return total


# =====================================================================
# outlier       - one string pulled out of a term family that holds together
# =====================================================================
@detector('outlier', 'chuỗi lạc khỏi gia đình thuật ngữ [--show N]')
def d_outlier(args, vi, src, _):
    """Day la mau that cua tan giong. `Cycle` giu o 81 chuoi. Neu con 1 chuoi
    goi no bang tu Viet, do khong phai 'dich sai theo cam tinh' - do la **keo
    nhom**: mot chuoi lot ra khoi 81 chuoi, va no se keo theo cac chuoi lot sau.

    Khong can biet 'dich dung la gi'. Chi can thay mot chuoi khac 81 chuoi."""
    V = HAN
    WORD = re.compile(r'[A-Za-zÀ-ỹ\u0100-\u024f]+')
    show = 25
    if '--show' in args:
        show = _int(args, args.index('--show') + 1, 25)

    def survey(term):
        rx = re.compile(r'(?<![A-Za-z])' + re.escape(term).replace(r'\ ', r'\s+')
                        + r'(?![A-Za-z])', re.I)
        kept, trans = [], []
        for k, v in vi.items():
            if k not in src or not V.search(v):
                continue
            if not rx.search(src[k]):
                continue
            (kept if rx.search(v) else trans).append(k)
        return kept, trans

    def distinctive(val, en):
        """Tu trong ban dich ma khong co trong ban goc - thuoc ve ban dich rieng."""
        en_w = {w.lower() for w in WORD.findall(en)}
        return [w for w in WORD.findall(val)
                if len(w) > 2 and w.lower() not in en_w]

    # moi tu viet hoa trong nguon, dem nhanh bang Counter
    counts = collections.Counter()
    for k in vi:
        if k not in src:
            continue
        for w in set(re.findall(r'[A-Za-z][A-Za-z-]+', src[k])):
            counts[w] += 1

    rows = []
    for term, _n in counts.most_common():
        if len(term) < 3 or not term[0].isupper():
            continue
        kept, trans = survey(term)
        if len(kept) < 3 or not trans:
            continue
        # 1 chuoi lech giua hang tram -> nghi keo nhom
        if len(trans) > max(2, len(kept) // 6):
            continue
        rows.append((len(trans), len(kept), term, kept, trans))

    rows.sort()
    print(f'{"n_dich":>6} {"n_giu":>6}  thuat ngu')
    print('-' * 64)
    for n_t, n_k, term, kept, trans in rows[:show]:
        flag = '  <<<' if n_t == 1 else ''
        print(f'{n_t:6} {n_k:6}  {term}{flag}')
    print(f'\n{len(rows)} thuat ngu co 1-2 chuoi lech giữ >=3 chuoi giu')

    if '--show' not in args:
        print('Chi tiet: python tools\\audit.py outlier --show 0')
        return len(rows)

    print('\n' + '=' * 70)
    for n_t, n_k, term, kept, trans in rows:
        print(f'\n### {term} — giu {n_k}, lich {n_t}')
        print(f'  (chu mau giu: {vi[kept[0]][:60]!r})')
        for k in trans[:4]:
            ds = distinctive(vi[k], src[k])
            print(f'  EN {src[k][:74]}')
            print(f'  VI {vi[k][:74]}')
            print(f'     rieng cua ban dich: {ds}')
            print(f'     con "giu" deu dung: {n_k} chuoi')
    return len(rows)


# =====================================================================
# same_en       - one English, two Vietnamese
# =====================================================================
@detector('same_en', 'một tiếng Anh nhưng hai bản dịch khác nhau')
def d_same_en(args, vi, src, _):
    """The mirror image of `dupes.py values`, and the more dangerous of the two.

    dupes.py values asks "do two different labels read the same on screen",
    which is a usability problem. This asks the opposite: "do two labels that
    Cubase stores under the same English read DIFFERENTLY on screen".

    WHAT IT MUST NOT REPORT. Round 193 ran this against keys/translation_
    original.xml and found all eleven of its findings to be FALSE ALARMS. Every
    one was a pair separated by the extractor's own DISAMBIGUATION marker, and
    the marker is the mechanism that is supposed to let two labels share one
    English:

        Key        <us>Key</us>          vi "Key"     (the musical key)
        Key[keycomms] <us>Key</us>       vi "Phím tắt" (the keyboard shortcut)

    German makes the distinction explicit - "Tonart" against "Taste" - and 8 of
    the 9 vendors translate that pair differently. Checking all eleven, the
    split runs from 8/9 down to 1/9, and not one of them wants them equal.

    The first version of this tool did the exact opposite of what its own
    comment said: it stripped the marker, required every key to reduce to the
    same bare string, and so KEPT precisely the marker pairs it claimed to be
    discarding. A comment that contradicts its code is worse than no comment,
    because it stops the next person checking. `DISAMBIG` below is the filter
    the comment described.

    `X[RM]` is a different marker and does NOT belong here: it is the same label
    shown in Cubase's Read Mode, all eight vendors translate the pair
    identically, and `audit.py rm` is the check that owns it. Including it would
    double-report one class and miss the other."""
    g = defaultdict(list)
    for k, u in src.items():
        if k in vi:
            g[u].append(k)

    # A trailing "[...]" or "{{...}}", i.e. the extractor's note to itself.
    # Anchored: "Direction [direction of a stem]" has the note at the end, and
    # "Page Height" inside "Height[Page Height]" has no brackets at all, so an
    # unanchored pattern is what made the old filter keep the wrong pairs.
    DISAMBIG = re.compile(r'\s*(?:\[[^\]]*\]|\{\{[^{}]*\}\})\s*$')

    def label_of(k):
        return DISAMBIG.sub('', k.strip()).strip().lower()

    rows = []
    for u, ks in g.items():
        if len(ks) < 2:
            continue
        vals = {vi[k] for k in ks}
        if len(vals) < 2:
            continue
        # Drop it when every key reduces to ONE label once its marker is gone -
        # that means a marker is the only thing telling them apart, which is the
        # mechanism working, not a defect.
        labels = {label_of(k) for k in ks}
        if len(labels) == 1 and any(DISAMBIG.search(k.strip()) for k in ks):
            continue
        # And drop it when the keys are genuinely DIFFERENT labels that share an
        # English only because column 2 was truncated into a neighbour -
        # "VST Connections" and "Audio Connections" both carry
        # "Audio Connections". Different labels must translate differently.
        if len(labels) > 1:
            continue
        rows.append((u, ks))

    rows.sort(key=lambda t: t[0])
    print(f'English strings given more than one Vietnamese: {len(rows)}\n')
    for u, ks in rows:
        print(f'  EN {u[:74]!r}')
        for k in sorted(ks, key=len):
            print(f'       {k[:66]!r}')
            print(f'         -> {vi[k][:66]!r}')
        print()
    return len(rows)


# =====================================================================
# numbers      - every number in the source must survive into the value
# =====================================================================
@detector('numbers', 'con so trong nguon phai con trong gia tri')
def d_numbers(args, vi, src, longest):
    """The dropped-clause class has turned up five times by hand (rounds 32, 38,
    38, 40, 44) and every time the lost text was the clause with a CONDITION or a
    COST in it. A number is the sharpest possible proxy for that: "44,1 kHz",
    "3 seconds", "10 %" cannot survive a paraphrase by accident.

    This is the one algorithmic detector in the set with no tuning and no
    exceptions, and round 194 measured it against the whole map: ONE hit, and
    that one is Cubase writing a European decimal comma in its own English
    ("44,1 kHz") where Vietnamese correctly writes "44.1". So the map is clean -
    but unlike every other clean result here, this one is earned by a rule that
    cannot be satisfied by luck.

    Two exclusions, both measured rather than guessed:
      - ordinals. "1st" -> "Thứ nhất" is CORRECT, and 5 of the first 23 hits in
        the first version of this probe were 1st..5th.
      - keys containing a `\\u` escape. "Agog\\u00F4 (High)" has the digits of an
        escaped code point in it, and the probe read them as the numbers 00 and 4.

    The lookbehind/lookahead matter too: `3.` at the end of a sentence is a
    number, so the trailing guard must reject a following WORD character and not
    a full stop. Getting that wrong made "Plug-in VST 3." look like a missing
    number, which is how the first probe reported two strings that are perfect.

    Numbers are compared on their DIGITS, not on their text. Cubase writes a
    European decimal comma in its own English - "44,1 kHz" - and Vietnamese
    writes "44.1 kHz"; those are the same number, and comparing text made the
    detector report the one string in the whole map where our translation is
    demonstrably right. Stripping the separator also handles the thousands comma
    correctly, so "1,000" and "1000" still match.
    """
    NUM = re.compile(r'(?<![\w.,])\d+(?:[.,]\d+)*(?!\w)')
    ORDINAL = re.compile(r'\b\d+(?:st|nd|rd|th)\b', re.I)

    def digits_only(text):
        return Counter(re.sub(r'\D', '', n) for n in NUM.findall(text))

    rows = []
    for k, v in vi.items():
        if '\\u' in k:
            continue                       # a key with an escaped codepoint in it
        en = _full(k, src, longest)        # NOT src[k]: column 2 is truncated
        if not en:
            continue
        miss = digits_only(ORDINAL.sub(' ', en)) - digits_only(v)
        if miss:
            rows.append((k, sorted(miss), en, v))

    rows.sort()
    print(f'values missing a number that the source has: {len(rows)}\n')
    for k, miss, en, v in rows:
        print(f'  {miss}  {k[:56]!r}')
        print(f'      EN {en[:130]!r}')
        print(f'      VI {v[:110]!r}')
    return len(rows)


# =====================================================================
# terms       - a term zh and jp both kept, that we translated
# =====================================================================
@detector('terms', 'thuat ngu ca zh va jp deu giu, ta lai dich [minhits]',
          needs_src=False)
def d_terms(args, vi, src, _):
    """A LEAD GENERATOR built out of the eight other vendors, and the only
    detector in the set that consults them.

    THE IDEA. Chinese and Japanese write in scripts that are not Latin. So every
    Latin run in their text is a word Steinberg chose NOT to translate - it is
    evidence, not accident. Take the words zh and jp have in common, and ask
    whether we kept them too. That is a question about POLICY, it needs no
    Vietnamese, and it is the only way round 194 found to ask a real question
    about terminology with a machine.

    WHAT IT IS NOT. zh and jp are a biased oracle, and the bias has to be named
    or the tool misleads. Both languages can translate a word Vietnamese should
    keep - 点击 is a perfectly good Chinese for "Click" - so agreement between
    them is not proof that the word must stay English. Round 194 measured the
    raw output: 96 values, and the largest cluster is "Click" x10, which
    AGENT.md round 54 settled the other way on purpose. Hence MINHITS: a term
    that appears once is a coincidence, a term that appears five times is a
    pattern.

    Measured with minhits 2: 25 values, 18 terms. Read them; do not auto-fix them.
    """
    MINHITS = _int(args, 0, 2)
    sib = _load_siblings()
    if not sib:
        print('keys/siblings.tsv not built - run: python tools\\build.py list ...')
        return 0

    LAT = re.compile(r"[A-Za-z0-9'\-]+")
    # Split at a letter/digit boundary as well as at punctuation. OMF2.0 and
    # OMF 2.0 are the same term, and without this the zh/jp text yields a bare
    # "OMF" while ours yields "OMF2" - so the detector reported three perfect
    # values as missing a term. German compounds (VST2PlugIn) hit it too.
    BOUNDARY = re.compile(r'([A-Za-z]+)(\d+)')
    STOPW = set("""the a an of in on at to for and or is are be been was were
    with by from into as if then else when while not no yes do does did can could
    will would shall should may might must you your this that these those it its
    their there here what which who how all any some more most other new old
    click please left right on off in out""".split())

    def words(text):
        out = set()
        for chunk in re.split(r"[^A-Za-z0-9'\-]+", text):
            chunk = BOUNDARY.sub(r'\1 \2', chunk)
            for w in chunk.replace('-', ' ').split():
                w = w.strip("'-.")
                if len(w) >= 3 and w.lower() not in STOPW:
                    out.add(w)
        return out

    # First pass: which terms does zh and jp agree on, and how often.
    want = Counter()
    for k, d in sib.items():
        zh, jp = d.get('zh', ''), d.get('jp', '')
        if not zh or not jp or k not in vi:
            continue
        common = words(zh) & words(jp)
        for w in common:
            want[w] += 1

    rows = []
    for k, v in vi.items():
        d = sib.get(k)
        if not d or not HAN.search(v):
            continue                       # a value with no Vietnamese at all
        zh, jp = d.get('zh', ''), d.get('jp', '')
        if not zh or not jp:
            continue
        common = {w for w in (words(zh) & words(jp)) if want[w] >= MINHITS}
        if not common:
            continue
        ours = {w.lower() for w in words(v)}
        miss = sorted(w for w in common if w.lower() not in ours)
        if miss:
            rows.append((k, miss, d.get('us', ''), v))

    tally = Counter(w for _, ms, _, _ in rows for w in ms)
    print(f'values where a term zh and jp both kept was translated: '
          f'{len(rows)}  (minhits={MINHITS}, {len(tally)} distinct terms)\n')
    print('--- most frequent ---')
    for w, n in tally.most_common(30):
        print(f'  {w:<22} {n}')
    print()
    for k, miss, en, v in rows[:60]:
        print(f'  {miss}  {k[:52]!r}')
        print(f'      EN {en[:112]!r}')
        print(f'      VI {v[:96]!r}')
    return len(rows)


# =====================================================================
# mojibake      - U+FFFD, and the repairs that are already applied
# =====================================================================
@detector('mojibake', 'ký tự hỏng U+FFFD trong bản dịch [--write để vá]', needs_src=False)
def d_mojibake(args, vi, src, _):
    """Round 122 found 34 values holding U+FFFD, the replacement character, from
    text pasted through a console that mangled a multi-byte Vietnamese
    character. The intent is recovered from context, so the repair is a table and
    not a rule - and the table is the record of what those 34 said.

    `--write` rewrites the batch files, not vi.json: vi.json is generated by
    merge_maps.py, so an edit made there is lost on the next merge."""
    MOJIBAKE = re.compile('\ufffd')

    REPAIRS = {
        'Agents: Undo Visibility Change': 'Agent: Hoàn tác thay đổi hiển thị',
        'Are you sure you want to remove this modulator?':
            'Bạn có chắc muốn gỡ bỏ Modulator này không?',
        'AudioWarp Quantize On/Off': 'Bật/Tắt AudioWarp Quantize',
        'Break Beams at Half-Bar Beat Boundaries':
            'Ngắt đuôi nốt tại ranh giới phách của nửa ô nhịp',
        'Cannot replace audio in this video file.\\nPlease close all applications '
        'that are using this video file and try again!':
            'Không thể thay thế Audio trong file Video này.\\n'
            'Vui lòng đóng tất cả ứng dụng đang dùng file Video này và thử lại!',
        'Clear Recent Paths': 'Xóa Recent Paths',
        'Clear Source Profile': 'Xóa Source Profile',
        'Clear all Messages': 'Xóa tất cả Messages',
        'Create New Chain': 'Tạo Chain',
        'Delete Script - Only Scripts located in Local Folder can be deleted':
            'Xóa Script - Chỉ các Script nằm trong thư mục cục bộ mới có thể xóa',
        'Drag divider to allow recording of Inserts.\\nInserts above the line are '
        'recorded.\\nInserts below the line are played back.':
            'Kéo vạch phân cách để cho phép ghi Insert.\\n'
            'Insert phía trên dòng kẻ được ghi.\\n'
            'Insert phía dưới dòng kẻ được phát lại.',
        'Edit Channel Settings': 'Sửa cài đặt Channel',
        "In some hand-copied lead sheets, the key signature is shown only at the "
        "beginning of the first bar, and it is hidden on subsequent systems. To "
        "follow this convention, choose 'Hide Key Signatures'.":
            'Trong một số bản tổng phổ chép tay, hóa biểu chỉ hiện ở đầu ô nhịp '
            'đầu tiên và ẩn ở các dòng nhạc tiếp theo. '
            "Để theo quy ước này, hãy chọn 'Ẩn hóa biểu'.",
        'Linked': 'Đã liên kết',
        "Meters' Fallback": 'Tốc độ hồi Meter',
        'No project is active. Please create or load a project.':
            'Không có Project nào đang hoạt động. Vui lòng tạo hoặc tải một Project.',
        'North-East': 'Đông Bắc',
        'Note is playing': 'Note đang phát',
        'On (Keep Sound Slot Active)': 'Bật (Giữ Sound Slot hoạt động)',
        'Placement Mode: Move a control on your MIDI controller or add it manually.':
            'Chế độ đặt: Di chuyển một điều khiển trên MIDI Controller '
            'hoặc thêm thủ công.',
        "Ruler Display Type has been changed to \\'Bar + Beats\\' and the Grid Type "
        "to \\'Use Quantize\\'.  This is required for Metronome Click Pattern Emphasis.":
            "Kiểu hiển thị thước đo đã đổi thành 'Bar + Beats' và loại Grid thành "
            "'Dùng Quantize'. Điều này là bắt buộc để nhấn trọng âm "
            'Pattern Click Metronome.',
        'Ruler Mode: Bars+Beats Linear': 'Chế độ thước đo: Bars+Beats tuyến tính',
        'Show Bar Number at Start of System for Bar Split Over Break':
            'Hiện số ô nhịp ở đầu dòng nhạc cho ô nhịp bị tách qua chỗ ngắt',
        'Show Normal Bar Number If Coincident with Start of Multi-Bar Rest Showing Range':
            'Hiện số ô nhịp bình thường nếu trùng với điểm bắt đầu '
            'của dải dấu lặng nhiều ô nhịp',
        'Single-line Instruments': 'Nhạc cụ 1 dòng kẻ',
        'Slashes without Stems': 'Gạch chéo không có thân nốt',
        'Some of the tracks that you want to delete contain data/events.\\n'
        'Do you really want to delete the tracks?':
            'Một số Track bạn muốn xóa có chứa dữ liệu/Event.\\n'
            'Bạn có thực sự muốn xóa các Track này không?',
        'The Control Room is disabled! Do you want to enable it?':
            'Control Room đang bị tắt! Bạn có muốn bật nó không?',
        'This will remove all columns in the Results list (except Name) for this '
        'combination of media types.':
            'Thao tác này sẽ gỡ bỏ tất cả cột trong danh sách kết quả '
            '(ngoại trừ Tên) cho tổ hợp loại Media này.',
        'Time Signature (changes the time signature before the project cursor position)':
            'Số chỉ nhịp (đổi số chỉ nhịp phía trước vị trí con trỏ Project)',
        'Use Reference Level (Press [ALT] to set)':
            'Dùng mức tham chiếu (Nhấn [ALT] để đặt)',
        'Warning: A control with the defined MIDI message already exists. Please '
        'change the MIDI message settings of one of the controls.':
            'Cảnh báo: Điều khiển với thông điệp MIDI đã định nghĩa đã tồn tại. '
            'Vui lòng đổi cài đặt thông điệp MIDI của một trong các điều khiển.',
        'Your changes will be lost and you will have to re-analyse this audio.':
            'Các thay đổi của bạn sẽ bị mất và bạn sẽ phải phân tích lại đoạn Audio này.',
        '\\nContext: ': '\\nNgữ cảnh: ',
    }

    BATCH_DIR = os.path.join(ROOT, 'translations', 'batches')
    broken = {k for k, v in vi.items() if MOJIBAKE.search(v)}
    print(f'values containing U+FFFD: {len(broken)}')
    missing = broken - set(REPAIRS)
    extra = set(REPAIRS) - broken
    if missing:
        print(f'  NO REPAIR DEFINED: {sorted(missing)}')
    if extra:
        print(f'  repair defined but value is clean: {sorted(extra)}')

    bad = [k for k, v in REPAIRS.items() if MOJIBAKE.search(v)]
    if bad:
        print(f'  REPAIR STILL BROKEN: {bad}')

    # A repair table LARGER than the set of broken values is not a finding: the
    # repairs were applied, so `extra` lists all 34 of them and the map is clean.
    # Counting it would report a healthy map as broken forever.
    if not broken and not missing and not bad:
        if '--write' not in args:
            print('\n(dry run - pass --write to apply)')
        return 0

    if bad:
        return len(broken) + len(missing) + len(bad)

    if '--write' not in args:
        print('\n(dry run - pass --write to apply)')
        return len(broken) + len(missing)

    import glob
    applied = 0
    for path in sorted(glob.glob(os.path.join(BATCH_DIR, '*.json'))):
        data = json.load(open(path, encoding='utf-8'))
        dirty = False
        for k, new in REPAIRS.items():
            if k in data and data[k] != new:
                data[k] = new
                dirty = True
                applied += 1
        if dirty:
            json.dump(data, open(path, 'w', encoding='utf-8'),
                      ensure_ascii=False, indent=2, sort_keys=True)
    print(f'applied {applied} repair(s)')
    return 0


# =====================================================================
ORDER = ['mojibake', 'leak', 'numbers', 'quality', 'fragments', 'same_en',
         'quotes', 'rm', 'gloss', 'collapsed', 'prefix', 'dropped', 'thin',
         'funcwords', 'opening', 'frame', 'frame_short', 'leftover', 'terms',
         'repeat_en', 'repeat_vi', 'pure_en', 'outlier', 'typos']

# A LEAD GENERATOR is a detector whose job is to hand you a list to READ, not to
# assert a defect. `fragments` reports 188 values every single run and 20 of
# them are worth looking at; `thin` reports 908 and 3 are. They never go quiet,
# so listing them under "defects" would train the reader to skip the summary -
# which is the failure mode AGENT.md §7 warns about. Keep them separate.
LEADS = {'fragments', 'thin', 'repeat_en', 'repeat_vi', 'frame', 'frame_short',
         'pure_en', 'outlier', 'typos', 'opening', 'terms'}

# Only these two exit non-zero on a finding, and that reproduces the exit codes
# the 24 separate scripts had. Round 193 measured this: making the other 20
# exit 1 as well would make AGENT.md §9 ("dừng ngay khi một bước báo lỗi") stop
# the pipeline on findings that have been read and judged ten times over.
STRICT_EXIT = {'leak', 'mojibake'}


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        print('=' * 72)
        w = max(len(n) for n in DETECTORS)
        for name in ORDER:
            tag = '  (dẫn đường)' if name in LEADS else ''
            print(f'  {name:<{w}}  {DETECTORS[name][1]}{tag}')
        print(f'\n{len(DETECTORS)} detectors.  Extra arguments go straight through,')
        print('e.g. `audit.py dropped 80`, `audit.py fragments --list`.')
        return 0

    if a[0] == '--all':
        # COUNT findings, do not read exit codes. Round 193 shipped a --all that
        # used the return value as a truthy test while twenty detectors returned
        # 0 by design, so it printed "detectors that fired: none" on a map that
        # same_en was reporting 11 findings for. A summary that cannot see is
        # worse than no summary.
        defects, leads = [], []
        for name in ORDER:
            print(f'\n===== {name} ' + '=' * (66 - len(name)))
            try:
                n = DETECTORS[name][0]([])
            except Exception as exc:                  # noqa: BLE001
                print(f'!! {name} crashed: {exc}')
                defects.append((name, -1))
                continue
            if n:
                (leads if name in LEADS else defects).append((name, n))

        print('\n' + '=' * 72)
        print(f'LỖI THẬT  ({len(ORDER) - len(LEADS)} bộ dò): '
              + ('không có' if not defects
                 else ', '.join(f'{n}={c}' for n, c in defects)))
        print(f'DẪN ĐƯỜNG ({len(LEADS)} bộ dò, luôn ra danh sách để đọc tay):')
        for n, c in leads:
            print(f'    {n:<12} {c}')
        if not leads:
            print('    (không có)')
        print('\nDẫn đường KHÔNG phải lỗi. Đọc nó bằng tay: `read.py`, `family.py`.')
        return 1 if defects else 0

    if a[0] not in DETECTORS:
        print(f'no detector named {a[0]!r}')
        print('run `python tools/audit.py` for the list')
        return 2
    n = DETECTORS[a[0]][0](a[1:])
    return 1 if (a[0] in STRICT_EXIT and n) else 0


if __name__ == '__main__':
    sys.exit(main())
