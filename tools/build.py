#!/usr/bin/env python3
"""Build the Vietnamese translation.xml, and the eight checks around it.

    python tools/build.py                     # the whole pipeline
    python tools/build.py <path-to-Cubase15.exe>

    python tools/build.py extract <exe> [out.xml]     TRANSLATION.XML out of the PE
    python tools/build.py list <in.xml> <out.tsv>     every Key/us pair to a TSV
    python tools/build.py prune [--dry-run]           drop keys Cubase never had
    python tools/build.py style [--verbose]           the 5 hard rules (AGENT.md)
    python tools/build.py punct                      ? ! ; ... \\n edge spaces
    python tools/build.py build <in> <out> <map.json> inject <vi>
    python tools/build.py strip <in> <out> [--keep us,vi]
    python tools/build.py validate <file.xml>

Nine scripts used to do this and each was runnable alone, which was the right
call while the build was being worked out. Round 193 put them in one file so that
"how is the file produced" has one answer you can read top to bottom, and every
step is still runnable on its own by name. Nothing outside the repo is touched -
use scripts/install.ps1 to deploy.

`tools/check_translation_build.py` stays a separate file on purpose: it is not a
step, it is the PROOF that the build did not alter anything else, and AGENT.md
§9 cites it by name.

DEFAULT EXE: E:\\Steinberg\\Cubase 15\\Cubase15.exe
"""
import glob
import json
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
PY = sys.executable

def T(*p):
    return os.path.join(ROOT, *p)

TSV = T('keys', 'all_strings.tsv')
MAP = T('translations', 'vi.json')
DEFAULT_EXE = r'E:\Steinberg\Cubase 15\Cubase15.exe'


def _load_tsv():
    if not os.path.exists(TSV):
        sys.exit(f'missing {TSV}\nrun: python tools/build.py list ...')
    src = {}
    for line in open(TSV, encoding='utf-8').read().splitlines()[1:]:
        if '\t' in line:
            k, u = line.split('\t', 1)
            src[k] = u
    return src


def _load_map():
    return json.load(open(MAP, encoding='utf-8'))


FORBIDDEN_PARENS = re.compile(r'\s*\([^()]+\)\s*$')


def check_value(key, val, src_text):
    """The five hard rules, applied to ONE value. [] means clean.

    `step_style` walks the map and calls this; the tests call it with a single
    value. Round 193 made the split because a rule that cannot be called on one
    value cannot be tested on one value - and the [RM] rule was unreachable from
    `check()`, which only knows the DAW-term table, so the round-66 case had no
    way to be asserted at all.

    The ORDER matters and is preserved from the original single loop: an empty
    value and a bad trailing parenthesis stop the other rules from also firing,
    so one wrong value produces one message rather than three.
    """
    from cubelib.placeholders import PLACEHOLDER

    if not isinstance(val, str) or not val.strip():
        return ['empty value']

    # Rule 1: no trailing dictionary parentheses unless the KEY has them
    if not FORBIDDEN_PARENS.search(key):
        mo = FORBIDDEN_PARENS.search(val)
        if mo:
            inside = mo.group(0).strip()[1:-1].strip()
            if inside.lower() in key.lower() or \
                    (len(inside) >= 3 and inside.isascii()):
                return [f'dictionary-style parenthesis {mo.group(0)!r} '
                        'forbidden by AGENT.md']

    out = []

    # Rule 2: no awkward literal Vietnamese of a standard DAW term
    for term in _forbidden(src_text, val):
        out.append(f'awkward translation of DAW term: keep {term!r} in English')

    # Rule 3: placeholders must match
    if src_text:
        want = sorted(PLACEHOLDER.findall(src_text))
        got = sorted(PLACEHOLDER.findall(val))
        if want != got:
            out.append(f'placeholder mismatch: source has {want}, '
                       f'translation has {got}')

    # Rule 5: the "[RM]" marker names the KEY, not the text
    if '[RM]' in val:
        out.append('the [RM] read-mode marker belongs to the key, '
                   'never to the translated text')

    return out


# =====================================================================
# extract - pull TRANSLATION.XML out of the Steinberg PE
# =====================================================================
def step_extract(a):
    """The UI string table is stored as plain, uncompressed UTF-8 XML in a PE
    resource, which is what makes the whole approach possible: Cubase reads
    <dir>/translation.xml from disk before falling back to the copy embedded in
    the executable, so no binary patch is needed to change the language."""
    from cubelib.pe import PE

    RESOURCE_NAME = 'TRANSLATION.XML'
    OUT_DEFAULT = 'translation.xml'

    if not a:
        sys.exit(f'usage: build.py extract <exe> [{OUT_DEFAULT}]')

    pe = PE(a[0])
    res = pe.find_resource(RESOURCE_NAME)
    if res is None:
        have = ', '.join(sorted({r.label for r in pe.resources()
                                 if any(isinstance(p, str) for p in r.path)}))
        pe.close()
        sys.exit(f'{RESOURCE_NAME} resource not found in {a[0]}\n'
                 f'named resources present: {have or "(none)"}')

    xml = pe.bin.slice(res.off, res.size)
    print(f'resource path: {res.label}')
    print(f'resource at file 0x{res.off:X}, {res.size:,} bytes')
    print(f'starts: {xml[:60]!r}')
    print(f'ends  : {xml[-40:]!r}')

    out = a[1] if len(a) > 1 else OUT_DEFAULT
    with open(out, 'wb') as fh:
        fh.write(xml)
    print(f'wrote {out} ({os.path.getsize(out):,} bytes)')

    text = xml.decode('utf-8', errors='replace')
    langs = re.findall(r'<language key="([^"]+)">([^<]*)</language>', text)
    print(f'\nlanguages ({len(langs)}): {langs}')

    keys = re.findall(r'<String Key="((?:[^"]|"(?!>))*?)">', text)
    print(f'String entries: {len(keys):,}')

    pairs = re.findall(r'<String Key="(.*?)">\s*<us>(.*?)</us>', text, re.S)
    same = sum(1 for k, u in pairs if k == u)
    print(f'Key == us  : {same:,} / {len(pairs):,}  '
          f'({same * 100 // max(1, len(pairs))}%)')

    print('\n--- main menus present? ---')
    for probe in ['File', 'Edit', 'Project', 'Audio', 'MIDI', 'Media', 'Transport',
                  'Devices', 'Window', 'Help', 'Studio', 'Scores', 'Plug-ins',
                  'Nudge', 'Mixer', 'VST Connections', 'Audio Connections']:
        m = re.search(r'<String Key="' + re.escape(probe) + r'">\s*<us>([^<]*)</us>',
                      text)
        print(f'  {probe:20} -> '
              f'{"HIT: " + m.group(1) if m else "not found as exact key"}')

    pe.close()


# =====================================================================
# list - every String Key / <us> pair into a TSV
# =====================================================================
def step_list(a):
    if len(a) < 2:
        sys.exit('usage: build.py list <in.xml> <out.tsv>')
    src, out = a[0], a[1]
    txt = open(src, encoding='utf-8').read()

    def unesc(s):
        return (s.replace('&lt;', '<').replace('&gt;', '>')
                 .replace('&quot;', '"').replace('&apos;', "'").replace('&amp;', '&'))

    rows = []
    for m in re.finditer(r'<String Key="(.*?)">(.*?)</String>', txt, re.S):
        u = re.search(r'<us>(.*?)</us>', m.group(2), re.S)
        rows.append((unesc(m.group(1)), unesc(u.group(1)) if u else ''))

    with open(out, 'w', encoding='utf-8', newline='') as f:
        f.write('key\tus\n')
        for k, u in rows:
            f.write(f'{k}\t{u}\n')

    print(f'wrote {out}: {len(rows):,} rows')

    short = [(k, u) for k, u in rows
             if 0 < len(u) <= 40 and '\\' not in u and '{' not in u]
    print(f'short (<=40 chars, no placeholders): {len(short):,}')

    # a quick view of the most "menu-like" ones
    menus = [(k, u) for k, u in rows
             if re.fullmatch(r'[A-Za-z][A-Za-z \-&/]{0,28}', u) and len(u) <= 30]
    print(f'menu-like candidates: {len(menus):,}')
    print('\n--- first 120 menu-like ---')
    for k, u in menus[:120]:
        print(f'  {u!r:34} key={k!r}')


# =====================================================================
# prune - map entries with no matching <String Key>
# =====================================================================
def step_prune(a):
    """Those are guesses that never existed in Cubase's table. Keeping them in
    vi.json means the build silently skips them and the map looks healthier than
    it is, so we park them in translations/unmatched.json for later."""
    OUT = T('translations', 'unmatched.json')
    dry = '--dry-run' in a
    src = _load_tsv()
    m = _load_map()

    bad = {k: v for k, v in m.items() if k not in src}
    good = {k: v for k, v in m.items() if k in src}

    print(f'{len(m)} entries: {len(good)} match a real <String Key>, '
          f'{len(bad)} do not')
    for k in bad:
        print(f'  no such key: {k!r}')

    if not dry and bad:
        prev = {}
        if os.path.exists(OUT):
            prev = json.load(open(OUT, encoding='utf-8'))
        prev.update(bad)
        json.dump(prev, open(OUT, 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=1, sort_keys=True)
        json.dump(good, open(MAP, 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=1, sort_keys=True)
        print(f'\nmoved {len(bad)} -> {os.path.relpath(OUT, ROOT)}; '
              f'vi.json now {len(good)} entries')

        # strip them from the batch files too, otherwise the next merge brings
        # them back
        for b in glob.glob(T('translations', 'batches', '*.json')):
            bd = json.load(open(b, encoding='utf-8'))
            dropped = [k for k in bad if k in bd]
            if not dropped:
                continue
            bd = {k: v for k, v in bd.items() if k not in bad}
            json.dump(bd, open(b, 'w', encoding='utf-8'),
                      ensure_ascii=False, indent=1, sort_keys=True)
            print(f'  pruned {len(dropped)} from {os.path.relpath(b, ROOT)}')

        print('Use tools/suggest_keys.py to find the real key for those.')
    elif dry and bad:
        print('\n(dry run, nothing written)')


# =====================================================================
# style - the five hard rules
# =====================================================================
def step_style(a):
    """Rules:
  1. NO trailing parenthetical glosses like "(<key>)" or "(English)".
  2. DAW technical loanwords (Track, Channel, Bus, Fader, Pan, Insert, Send,
     Metronome, Click, Marker, Locator, Automation, Clip, Event, Quantize,
     Snap, Grid, Bounce, Render, Freeze, Warp, ASIO, VST, MIDI...) stay English.
  3. %-placeholders (%s, %d, %.3f, etc.) must survive intact.
  4. No empty values.
  5. No value may contain the "[RM]" marker.

Rule 5 is rule 6 of a family of four, and it is the only one that is not about
style. Cubase's extractor makes a second copy of a label for its read-mode
display and names it "X[RM]"; the two keys are separate <String> entries with the
same English, and every one of the eight vendors translates them IDENTICALLY and
with no marker in the value. Round 66 found eleven values carrying it, which
means the word "[RM]" would have been drawn on screen next to the label."""
    verbose = '--verbose' in a
    src = _load_tsv()
    m = _load_map()

    errors, warns = [], []
    for key, val in sorted(m.items()):
        for why in check_value(key, val, src.get(key, '')):
            errors.append((key, val, why))

    print(f'style check: {len(m)} entries in {os.path.relpath(MAP, ROOT)}')

    if warns:
        print(f'\n{len(warns)} warning(s):')
        for k, v, why in warns:
            print(f'  {k!r} = {v!r}\n      {why}')

    if errors:
        print(f'\n{len(errors)} VIOLATION(S):')
        for k, v, why in errors[:25]:
            print(f'  {k!r} = {v!r}\n      -> {why}')
        if len(errors) > 25:
            print(f'  ... and {len(errors)-25} more')
        print('\nSee AGENT.md for natural hybrid English-Vietnamese guidelines.')
        sys.exit(1)

    print('\nOK - every value follows the natural hybrid style (AGENT.md)')
    if verbose:
        for k, v in sorted(m.items())[:40]:
            print(f'  {k!r:44} -> {v}')


# =====================================================================
# punct - every mark of punctuation must survive
# =====================================================================
def step_punct(a):
    """AGENT.md and the project brief both require it - "bao toan 100%
placeholder, dau hai cham, ?/!/., dau ba cham" - and nothing used to check it.
check_style enforces placeholders, no trailing gloss, no empty value, no [RM]
marker and the DAW-term list. Punctuation was always assumed.

The reason it needs its own check is that a lost mark is invisible in a long
value: a missing "?" at the end of a question still reads as a question, and a
lost "..." after a menu command still reads as a menu command. It shows up in
the UI as a missing ellipsis on a button, and nobody would report it."""
    src = _load_tsv()
    vi = _load_map()

    # a run of three or more dots is one ellipsis, however long the source wrote it
    ELL = re.compile(r'\.{3,}')

    def counts(s):
        return {'?': s.count('?'), '!': s.count('!'), ';': s.count(';'),
                '...': len(ELL.findall(s))}

    bad = []
    for k, v in sorted(vi.items()):
        en = src.get(k)
        if en is None:
            continue
        a2, b2 = counts(en), counts(v)
        why = None
        for mark in ('?', '!', ';', '...'):
            if a2[mark] != b2[mark]:
                why = (mark, a2[mark], b2[mark])
                break
        # the last two requirements nobody had checked either: the LINE BREAKS
        # and the leading and trailing whitespace. A lost \n turns a two-sentence
        # tooltip into one run-on line, and a lost trailing space silently
        # changes what Cubase draws, because the XML preserves it.
        if why is None:
            if en.count('\\n') != v.count('\\n'):
                why = ('\\n', en.count('\\n'), v.count('\\n'))
            elif (en[:1].isspace()) != (v[:1].isspace()):
                why = ('leading space', int(bool(en[:1].isspace())),
                       int(bool(v[:1].isspace())))
            elif (en[-1:].isspace()) != (v[-1:].isspace()):
                why = ('trailing space', int(bool(en[-1:].isspace())),
                       int(bool(v[-1:].isspace())))
        if why:
            bad.append((k, why[0], why[1], why[2], en, v))

    print('values whose punctuation, line breaks or edge whitespace differ '
          f'from the source: {len(bad)}\n')
    for k, mark, want, got, en, v in bad[:40]:
        print(f'  {mark!r} source {want} -> value {got}')
        print(f'      EN {en[:74]!r}')
        print(f'      VI {v[:74]!r}')
    if len(bad) > 40:
        print(f'  ... and {len(bad) - 40} more')
    sys.exit(1 if bad else 0)


# =====================================================================
# build - inject <vi> into a Steinberg translation.xml
# =====================================================================
def step_build(a):
    if len(a) < 3:
        sys.exit('usage: build.py build <in.xml> <out.xml> <map.json> [--langname X]')
    src, dst, mapfile = a[0], a[1], a[2]
    langname = 'Vietnamese'
    if '--langname' in a:
        langname = a[a.index('--langname') + 1]
    lang = 'vi'

    txt = open(src, 'r', encoding='utf-8').read()
    tmap = json.load(open(mapfile, 'r', encoding='utf-8'))

    def esc(s):
        return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

    # 1) register the language.
    #
    # The indentation is taken from the sibling <language> lines rather than
    # hardcoded.  The old version emitted a literal two-tab indent, which landed
    # one tab deeper than its nine siblings because those two tabs of existing
    # indentation were still in front of the insertion point.  XML does not
    # care; a diff of 10,737 entries does.
    if f'<language key="{lang}">' not in txt:
        existing = re.findall(r'\n(\t*)<language key="', txt)
        if not existing:
            sys.exit(f'no <language key=...> lines found in {src}')
        depth = existing[-1]
        # Anchor on the whole closing line, not on the tag text.  Replacing just
        # '</LanguageTable>' leaves that tag's own leading tab in front of the new
        # line, which is how the earlier attempt ended up one tab too deep.
        m_close = re.search(r'\n(\t*)</LanguageTable>', txt)
        if not m_close:
            sys.exit(f'no </LanguageTable> found in {src}')
        txt = (txt[:m_close.start()]
               + f'\n{depth}<language key="{lang}">{langname}</language>'
               + m_close.group(0)
               + txt[m_close.end():])
        print(f'+ registered language {lang} = {langname} at '
              f'{len(depth)} tab(s), matching its nine siblings')

    # 2) add <vi> to each String that we have a translation for
    added = 0
    matched = set()
    out = []
    pat = re.compile(r'<String Key="(.*?)">(.*?)</String>', re.S)

    # The depth the nine shipped language tags sit at inside a <String>.  Taken
    # from the file, so the injected <vi> is a child of <String> exactly like its
    # siblings.
    _depths = re.findall(r'\n(\t*)<\w\w>', txt)
    TAG_DEPTH = (max(set(_depths), key=_depths.count) if _depths else '\t\t\t')
    for m in pat.finditer(txt):
        key, body = m.group(1), m.group(2)
        raw_key = (key.replace('&lt;', '<').replace('&gt;', '>')
                      .replace('&quot;', '"').replace('&amp;', '&'))
        if raw_key in tmap:
            matched.add(raw_key)
            vi = esc(tmap[raw_key])
            if re.search(rf'<{lang}>.*?</{lang}>', body, re.S):
                continue
            # Where to insert, and what to insert.
            #
            # The text just before </String> already ends with a newline and that
            # tag's own indentation, so inserting at the position of </String>
            # itself and supplying a leading newline leaves that indentation
            # orphaned on a line of its own.  The offset therefore moves back
            # over it, and the block brings its own newline and depth.  An
            # earlier attempt did not, and check_translation_build.py caught it:
            # the stripped output was 32,211 characters longer than the
            # original, which is three per entry.
            _close = re.search(r'\n(\t*)</String>\s*$', m.group(0))
            close_depth = _close.group(1) if _close else TAG_DEPTH
            insert_at = m.end() - len('</String>') - len(close_depth) - 1
            out.append((insert_at, f'\n{TAG_DEPTH}<{lang}>{vi}</{lang}>'))
            added += 1

    print(f'  <{lang}> block at {len(TAG_DEPTH)} tab(s), matching its nine '
          'siblings')

    for off, ins in reversed(out):
        txt = txt[:off] + ins + txt[off:]

    unmatched = [k for k in tmap if k not in matched]
    if unmatched:
        print(f'! {len(unmatched)} map entries had no matching <String Key>:')
        for k in unmatched:
            print(f'    - {k!r}')

    with open(dst, 'w', encoding='utf-8', newline='') as f:
        f.write(txt)

    print(f'+ injected <{lang}> into {added:,} strings')
    print(f'  map entries : {len(tmap):,}')
    print(f'  output      : {os.path.getsize(dst):,} bytes '
          f'(was {os.path.getsize(src):,})')


# =====================================================================
# strip - English and Vietnamese only
# =====================================================================
def step_strip(a):
    """Cubase's file carries nine languages for every one of its 10,737 strings,
and the eight this project does not use account for about 82% of the text:

    ru 544,420   jp 534,556   fr 471,434   it 470,224
    es 447,688   pt 443,998   de 433,529   zh 361,083     bytes
    us 379,104   vi 443,091                                 bytes

WHY IT IS A TARGET AND NOT A REPLACEMENT. The original has exactly nine language
elements in all 10,737 entries - not one entry anywhere is missing one, so the
file is perfectly uniform and a reduced one is a shape Cubase has never been
handed. Two things make that recoverable rather than risky: keys/translation_
original.xml is the source this reads, it is in git, and install.ps1 writes a
.bak beside every file it overwrites and has -Action uninstall. build.py still
produces the full file; this one is opt-in.

WHAT IS TOUCHED. Only the language ELEMENTS inside each <String> are removed,
and only those whose key is not in --keep. Nothing else is rewritten."""
    if len(a) < 2:
        sys.exit('usage: build.py strip <in.xml> <out.xml> [--keep us,vi]')
    src, dst = a[0], a[1]
    keep = {'us', 'vi'}
    if '--keep' in a:
        keep = {s.strip() for s in a[a.index('--keep') + 1].split(',')}

    txt = open(src, 'r', encoding='utf-8').read()

    # Every language element. The indentation is three tabs inside a <String>:
    #
    #    \t\t<String Key="...">
    #    \t\t\t<us>...</us>
    #
    # Only elements at THREE tabs are inside a <String>. The <LanguageTable>
    # entries are at two tabs and must survive - they are what makes
    # "Vietnamese" appear in the language list at all.
    ELEM = re.compile(r'\n\t\t\t<(\w+)>(.*?)</\1>', re.S)
    seen = set()
    removed = [0]

    def prune(m):
        seen.add(m.group(1))
        if m.group(1) in keep:
            return m.group(0)
        removed[0] += 1
        return ''

    out = ELEM.sub(prune, txt)

    # self-closing <de/> style, if the file ever uses one
    EMPTY = re.compile(r'\n\t\t\t<(\w+)\s*/>')

    def prune_empty(m):
        seen.add(m.group(1))
        if m.group(1) in keep:
            return m.group(0)
        removed[0] += 1
        return ''

    out = EMPTY.sub(prune_empty, out)

    # The <LanguageTable> lists the languages Cubase will OFFER in
    # Edit > Preferences > General > Language. If it keeps rows for languages
    # whose strings are gone, the dropdown offers German and French and then has
    # nothing for them. Dropping the rows makes the file consistently
    # two-language. This is the one edit that is NOT a pure deletion of a
    # <String> child, and it is why the file is a separate target rather than a
    # change to the build: the language list is what puts Vietnamese in the menu.
    if '--keep-langtable' not in a:
        ROW = re.compile(r'\n\t\t<language key="(\w+)">([^<]*)</language>')
        dropped = []

        def prune_row(m):
            if m.group(1) in keep:
                return m.group(0)
            dropped.append((m.group(1), m.group(2)))
            return ''

        out = ROW.sub(prune_row, out)
        print('language rows dropped from the table: '
              f'{len(dropped)}  ({", ".join(k for k, _ in dropped)})')

    with open(dst, 'w', encoding='utf-8', newline='') as f:
        f.write(out)

    x, y = os.path.getsize(src), os.path.getsize(dst)
    print(f'kept      : {sorted(keep)}')
    print(f'languages found: {sorted(seen)}')
    print(f'elements removed: {removed[0]:,}')
    print(f'{x:,} bytes  ->  {y:,} bytes   ({100 * y / x:.0f}%)')

    # a String that lost its <us> is broken, so check none did
    n_str = out.count('<String Key=')
    bad = 0
    for m in re.finditer(r'<String Key="[^"]*">(.*?)</String>', out, re.S):
        if '<us>' not in m.group(1):
            bad += 1
    print(f'String entries: {n_str:,}   without <us>: {bad}')
    sys.exit(1 if bad else 0)


# =====================================================================
# validate - a generated translation.xml
# =====================================================================
def step_validate(a):
    if not a:
        sys.exit('usage: build.py validate <file.xml>')
    path = a[0]
    print(f'validating {path} ...')
    try:
        tree = ET.parse(path)
    except ET.ParseError as e:
        print(f'  XML PARSE ERROR: {e}')
        sys.exit(1)
    print('  XML is well-formed  OK')

    root = tree.getroot()
    print(f'  root element: <{root.tag}>')

    langs = [e.get('key') for e in root.findall('./LanguageTable/language')]
    print(f'  LanguageTable ({len(langs)}): {langs}')
    if 'vi' not in langs:
        print('  !! vi NOT registered')
        sys.exit(1)
    print('  vi registered  OK')

    strings = root.findall('./StringTable/String')
    print(f'  StringTable entries: {len(strings):,}')

    counts = {}
    vi_empty = 0
    for s in strings:
        for child in s:
            if child.tag == 'String':
                continue
            counts[child.tag] = counts.get(child.tag, 0) + 1
            if child.tag == 'vi' and not (child.text or '').strip():
                vi_empty += 1
    print('  children per language:')
    for k, v in sorted(counts.items(), key=lambda x: -x[1]):
        print(f'    <{k}> : {v:,}')
    if vi_empty:
        print(f'  !! {vi_empty} empty <vi> elements')

    # spot-check a few known menus per AGENT.md
    checks = {'File': 'File', 'Edit': 'Sửa', 'Transport': 'Transport',
              'Devices': 'Thiết bị'}
    print('  spot-check:')
    for s in strings:
        k = s.get('Key')
        if k in checks:
            vi = s.find('vi')
            got = (vi.text if vi is not None else None)
            mark = 'OK' if got == checks[k] else 'MISMATCH'
            print(f'    {k:12} -> {got!r}  [{mark}]')
    print('\nVALIDATION PASSED' if not vi_empty
          else '\nVALIDATION PASSED (with empty entries)')


# =====================================================================
# the whole pipeline
# =====================================================================
def pipeline(exe):
    os.makedirs(T('keys'), exist_ok=True)
    os.makedirs(T('build'), exist_ok=True)
    base, tsv, out = T('keys', 'translation_original.xml'), TSV, T('build', 'translation_vi.xml')

    def run(args, title, script):
        print(f'\n=== {title} ===')
        r = subprocess.run([PY, T('tools', script)] + args, cwd=ROOT)
        if r.returncode != 0:
            print(f'!! {title} failed (exit {r.returncode})')
            sys.exit(r.returncode)

    def sub(args, title):
        print(f'\n=== {title} ===')
        r = subprocess.run([PY, os.path.join(HERE, 'build.py')] + args, cwd=ROOT)
        if r.returncode != 0:
            print(f'!! {title} failed (exit {r.returncode})')
            sys.exit(r.returncode)

    sub(['extract', exe, base], 'extract TRANSLATION.XML from exe')
    sub(['list', base, tsv], 'list all strings')
    run(['--check'], 'check translation maps', 'merge_maps.py')
    sub(['prune', '--dry-run'], 'check every map key exists in Cubase')
    sub(['style'], 'enforce hybrid style (AGENT.md)')
    sub(['punct'], 'check ? ! ; ... line breaks edge spaces')
    sub(['build', base, out, MAP], 'build Vietnamese translation.xml')
    # Assert the whole premise mechanically: the built file is the original plus
    # <vi>, and removing the injected lines gives the original back byte for
    # byte. install.ps1 used to claim this in prose; the claim is now checked.
    run([], 'prove the build is original + vi', 'check_translation_build.py')
    # a second target: the same file with the eight unused languages removed.
    # install.ps1 deploys this one by default.  Note that "Cubase reads it
    # correctly" is a claim about the *file* - see docs/RESEARCH.md; nothing in
    # the repo records the full variant ever being tried at runtime, and the
    # parser carries no language table, so there is no mechanism by which ten
    # blocks would read worse than two.
    sub(['strip', out, T('build', 'translation_vi_en.xml')],
        'build the English + Vietnamese only variant')
    sub(['validate', out], 'validate output')

    print(f'\nDone. -> {os.path.relpath(out, ROOT)}  '
          f'({os.path.getsize(out):,} bytes)')
    print('Deploy with:  powershell -File scripts\\install.ps1 -Action install')


# =====================================================================
# termspec - terms_do_not_translate.json as rules
# =====================================================================
# Boc terms_do_not_translate.json thanh luat.
#
# Hai loai mau:
#
#     "Track": ["\\brãnh\\b"]                     sai o moi ngu canh
#     "Bypass": [{"vi": "\\bbỏ qua\\b",
#                 "src": "\\bbypass\\b"}]          chi sai khi NGUON khop src
#
# Loai thu hai khong phai chuyen phuc tap hoa. `Bypass -> bo qua` la sai
# (13 chuoi da sua o dot 72), nhung `Ignore -> bo qua` la dung va co 23
# chuoi nhu vay trong ban dich. Mot mau vo dieu kien se chan het 23 chuoi
# dung do, va mot bo do bao dong gia thi khong ai doc nua (AGENT.md §7).
#
# This block lives here because `style` is its only caller in the tools, but the
# TESTS also import rules_for_tests() - a pattern with no condition can be tested
# in both directions without a source, and that is how the 64 DAW terms were
# taught rather than merely listed.
_SPEC = T('terms_do_not_translate.json')


def spec():
    return json.load(open(_SPEC, encoding='utf-8'))


def _compile(p):
    if isinstance(p, str):
        return None, re.compile(p, re.I)
    return re.compile(p['src'], re.I), re.compile(p['vi'], re.I)


def rules_for_style():
    """[(rx_src | None, rx_vi, term)] - rx_src None nghia la moi ngu canh."""
    out = []
    for term, pats in spec()['forbidden'].items():
        if term.startswith('_'):
            continue
        for p in pats:
            rx_src, rx_vi = _compile(p)
            out.append((rx_src, rx_vi, term))
    return out


def rules_for_tests():
    """[(term, compiled_vi)] - chi mau vo dieu kien, test duoc doc lap."""
    out = []
    for term, pats in spec()['forbidden'].items():
        if term.startswith('_'):
            continue
        for p in pats:
            if isinstance(p, str):
                out.append((term, re.compile(p, re.I)))
    return out


def check(src_text, val):
    """[(term, matched_text)] - cac luat bi vi pham boi (src, val).

    This is what the tests call, and it is deliberately the SAME code path as
    `style`, so a rule cannot pass a test and still fail the build."""
    hits = []
    for rx_src, rx_vi, term in rules_for_style():
        if rx_src is not None and not rx_src.search(src_text):
            continue
        m = rx_vi.search(val)
        if m:
            hits.append((term, m.group(0)))
    return hits


_rules = None


def _forbidden(src_text, val):
    global _rules
    if _rules is None:
        _rules = rules_for_style()
    hits = []
    for rx_src, rx_vi, term in _rules:
        if rx_src is not None and not rx_src.search(src_text):
            continue
        if rx_vi.search(val):
            hits.append(term)
    return hits


STEPS = {
    'extract': step_extract, 'list': step_list, 'prune': step_prune,
    'style': step_style, 'punct': step_punct, 'build': step_build,
    'strip': step_strip, 'validate': step_validate,
}

if __name__ == '__main__':
    argv = sys.argv[1:]
    if not argv or argv[0] not in STEPS:
        pipeline(argv[0] if argv else DEFAULT_EXE)
    else:
        STEPS[argv[0]](argv[1:])