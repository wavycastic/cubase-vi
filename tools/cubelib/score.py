"""The Score Editor's own localisation format: `instrumentnames_XX.xml`.

Cubase's `translation.xml` is only half the problem.  The Score Editor -
Steinberg's Dorico engine, embedded as `ScoringEngine.dll` - localises itself
from `Components/ScoringEngine/l10n`, which holds one instrument-name XML per
language alongside the Qt catalogues in `qm.py`.  `ScoringEngine.dll` globs
that folder, so a Vietnamese file is authoring work, not a binary patch.

What the file looks like
-----------------------
    <kScoreLibrary>
      <instrumentNames>
        <language>kEnglish</language>
        <entities array="true">
          <InstrumentNameEntityDefinition>
            <name>Accordion</name>              <- entity-level, never localised
            <entityID>instrumentname.keyboard.accordion</entityID>
            <parentEntityID/>
            <inheritanceMask>0</inheritanceMask>
            <data>
              <uiName>Accordion</uiName>
              <singularFullName>Accordion</singularFullName>
              ...
              <gender>kNeutral</gender>
              <language>kEnglish</language>
            </data>
          </InstrumentNameEntityDefinition>

All nine shipped languages have exactly the same 624 entity IDs, and
`parentEntityID` / `inheritanceMask` are byte-identical across them, so the
English file is a complete template.  Only the five name fields inside `<data>`
are localised, plus the `<language>` marker (625 occurrences: one per entity
plus one at the top).

Why this splices text instead of re-serialising
-----------------------------------------------
The file uses CRLF throughout, tab indentation, a `<?xml version="1.0" ?>`
header with a space before the `?>`, and writes empty fields as `<x/>`.  It
also does not keep its child elements in a fixed order - `aluphone` puts
`<name>` before `<entityID>` where `accordion` puts it after.  Re-serialising
through ElementTree would rewrite every one of those details, so instead the
file is edited as text inside each entity block and the result is then parsed
and checked, which gets fidelity without guessing at a serialiser's quirks.
"""
import os
import re
import xml.etree.ElementTree as ET
from xml.sax.saxutils import unescape as _xml_unescape

#: The five fields inside <data> that carry user-visible text.
LOCALISED_FIELDS = ('uiName', 'singularFullName', 'singularShortName',
                    'pluralFullName', 'pluralShortName')

#: Fields that must survive byte-for-byte.
STRUCTURAL_FIELDS = ('entityID', 'parentEntityID', 'inheritanceMask')

TARGET_LANGUAGE = 'kVietnamese'

ENTITY_BLOCK = re.compile(
    r'[ \t]*<InstrumentNameEntityDefinition>(?P<body>.*?)'
    r'</InstrumentNameEntityDefinition>\r?\n',
    re.DOTALL)

#: <tag>text</tag> or the self-closing <tag/>
FIELD = re.compile(r'<(?P<tag>[A-Za-z]+)(?:\s[^>]*)?'
                   r'(?:/>|>(?P<text>[^<]*)</(?P=tag)>)')

#: the <language> marker, e.g. kEnglish
LANGUAGE = re.compile(r'<language>([^<]*)</language>')

#: Characters that must never reach the file.  The repo has been bitten by a
#: stray 0x07 from a shell round-trip corrupting a translation, so they are
#: rejected here rather than discovered in Cubase.
#:
#: A set of one-character strings, not a dict keyed by code point.  It was a
#: `dict.fromkeys` of ints, and the guard tested `c in FORBIDDEN` with `c` a
#: character, so it never matched anything and `check_text` accepted a NUL
#: byte.  `test_score.py::TestCheckText::test_rejects` is what found it.
FORBIDDEN = frozenset(chr(c) for c in range(0x20)
                      if c not in (0x09, 0x0A, 0x0D)) | {chr(0x7F)}

#: The only tails a Vietnamese value may drop from its English key.  A key
#: that ends in one of these is a plural, and Vietnamese writes it the same
#: way as the singular.
PLURAL_TAIL = ('s', 'es', 'n')


class ScoreError(ValueError):
    pass


def xml_escape(text):
    return (text.replace('&', '&amp;').replace('<', '&lt;')
                .replace('>', '&gt;'))


def xml_unescape(text):
    return _xml_unescape(text, {'&apos;': "'", '&quot;': '"'})


def check_text(text, what='string'):
    """Reject text that would corrupt the file or the UI."""
    if not text:
        raise ScoreError(f'{what} is empty')
    if '\ufffd' in text:
        raise ScoreError(f'{what} contains U+FFFD: {text!r}')
    bad = sorted({c for c in text if c in FORBIDDEN})
    if bad:
        raise ScoreError(f'{what} contains control characters '
                         f'{[hex(ord(c)) for c in bad]}: {text!r}')
    if text != text.strip():
        raise ScoreError(f'{what} has leading/trailing whitespace: {text!r}')
    return text


class Entity:
    """One `InstrumentNameEntityDefinition`, tied to its span in the source.

    `block` is the whole element including its opening tag, because that is
    what has to be spliced back out; the field offsets used for rewriting are
    character offsets into it.
    """

    def __init__(self, entity_id, start, end, block, fields):
        self.entity_id = entity_id
        self.start = start
        self.end = end
        self.block = block
        self.fields = fields          # field name -> English text ('' if empty)

    def __repr__(self):
        return f'<Entity {self.entity_id!r} {self.fields.get("uiName")!r}>'


def read(path):
    """Parse the file into `(raw_text, [Entity, ...])`.

    The raw text is kept so the writer can splice into it; the entities carry
    the character span of their block within it.
    """
    try:
        with open(path, encoding='utf-8', newline='') as fh:
            text = fh.read()
    except OSError as exc:
        raise ScoreError(f'cannot read {path}: {exc}') from exc
    except UnicodeDecodeError as exc:
        raise ScoreError(f'{path} is not UTF-8: {exc}') from exc
    out = []
    for m in ENTITY_BLOCK.finditer(text):
        block = m.group(0)
        fields, eid = {}, ''
        for f in FIELD.finditer(block):
            tag = f.group('tag')
            if tag == 'entityID':
                eid = xml_unescape(f.group('text') or '')
            elif tag in LOCALISED_FIELDS:
                fields[tag] = xml_unescape(f.group('text') or '')
        if not eid:
            raise ScoreError(f'entity without an entityID in {path}: '
                             f'{block[:80]!r}')
        missing = [f for f in LOCALISED_FIELDS if f not in fields]
        if missing:
            raise ScoreError(f'{eid}: no {", ".join(missing)}')
        out.append(Entity(eid, m.start(), m.end(), block, fields))
    if not out:
        raise ScoreError(f'no entities found in {path}')
    return text, out


def verify(path):
    """Parse the file with a real XML parser and report what it holds.

    Used as a self-check after a textual rewrite: if the splice produced
    something that is not well-formed, or lost an entity, this is what notices.
    """
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        raise ScoreError(f'{path} is not well-formed XML: {exc}') from exc
    lang = root.findtext('./instrumentNames/language')
    ids, filled = [], 0
    for e in root.iter('InstrumentNameEntityDefinition'):
        eid = e.findtext('entityID')
        ids.append(eid)
        d = e.find('data')
        if d is not None and any(d.findtext(f) for f in LOCALISED_FIELDS):
            filled += 1
    return {'language': lang, 'entities': len(ids), 'unique': len(set(ids)),
            'with_names': filled, 'root': root.tag}


def build(source_path, mapping, out_path, language=TARGET_LANGUAGE,
          expect=None):
    """Write a localised copy of `source_path` using `mapping`.

    `mapping` is `{english_text: translated_text}`.  Anything absent keeps its
    English text, which is how a partly-translated catalogue stays usable.

    Returns a report dict; raises ScoreError if the result is not well-formed
    or if an entry of `mapping` is not actually needed.
    """
    text, entities = read(source_path)

    unused = set(mapping)
    out, pos, replaced, missing = [], 0, 0, []
    for ent in entities:
        out.append(text[pos:ent.start])
        block = ent.block
        # Descending offset order, so that replacing a later field cannot move
        # the span of one still to come.
        for tag, value in sorted(ent.fields.items(),
                                 key=lambda kv: -_span(ent.block, kv[0])[0]):
            start, end = _span(block, tag)
            if value in mapping:
                unused.discard(value)
                new = mapping[value]
                # An identity mapping introduces nothing, so it is not worth
                # checking - the text came from the source.  It has to be
                # allowed, because a few source fields carry a trailing
                # space (`<O. M. >`) and leaving them alone is the answer.
                if new != value:
                    new = check_text(new, f'{ent.entity_id}/{tag}')
                replaced += 1
                if not new:
                    missing.append(f'{ent.entity_id}/{tag}')
                    replacement = f'<{tag}/>'
                else:
                    replacement = f'<{tag}>{xml_escape(new)}</{tag}>'
            else:
                # Untouched: put back the exact original slice, escapes and
                # all, so an untranslated field is bit-for-bit what it was.
                replacement = block[start:end]
            block = block[:start] + replacement + block[end:]
        out.append(block)
        pos = ent.end
    out.append(text[pos:])
    result = ''.join(out)

    # The language marker appears once at the top and once per entity: 625 in
    # every shipped file.  They are all rewritten to the target, because the
    # shipped files are not internally consistent - see `mis_tagged`.
    markers = LANGUAGE.findall(result)
    if not markers:
        raise ScoreError('source file declares no <language> marker')
    if language in markers and set(markers) == {language}:
        raise ScoreError(f'target language {language!r} equals the source')
    result = LANGUAGE.sub(f'<language>{language}</language>', result)
    n_lang = len(markers)

    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, 'w', encoding='utf-8', newline='') as fh:
        fh.write(result)

    report = verify(out_path)
    if expect is not None and report['entities'] != expect:
        raise ScoreError(f'{out_path}: {report["entities"]} entities, '
                         f'expected {expect}')
    if report['language'] != language:
        raise ScoreError(f'{out_path}: language is {report["language"]!r}, '
                         f'expected {language!r}')
    if missing:
        raise ScoreError(f'{len(missing)} field(s) came out empty, e.g. '
                         + ', '.join(missing[:5]))
    report.update(replaced=replaced, language_markers=n_lang,
                  mis_tagged=sorted({m for m in markers if m != language}),
                  unused=sorted(unused))
    return report


def _span(block, tag):
    """Character span of a whole field element, tags included.

    The span covers `<tag>`, the value and `</tag>` - or just `<tag/>` for an
    empty field - so that a replacement is always a complete element rather
    than a value dropped inside the original one.
    """
    m = re.search(rf'<{tag}(?:\s[^>]*)?(?:/>|>.*?</{tag}>)',
                  block, re.DOTALL)
    if not m:
        raise ScoreError(f'field {tag} not found')
    return m.start(), m.end()


def source_strings(entities):
    """The distinct English strings a translator has to deal with.

    Maps each string to the list of entity IDs that use it, deduplicated per
    entity.  `uiName` and `singularFullName` hold the same text in every
    entity, so without that the reuse count would be twice the number of
    instruments a translation reaches, and `--status` would overstate the work
    each string saves.
    """
    seen = {}
    for ent in entities:
        for value in ent.fields.values():
            if value and ent.entity_id not in seen.get(value, ()):
                seen.setdefault(value, []).append(ent.entity_id)
    return seen


#: Pairs where a plural and its singular legitimately denote different things,
#: so the agreement rule below must not fire.  `Voice` is one vocal line and
#: `Voices` is the section that the Score Editor shows - the main UI table
#: already settled it that way and both values are seeds, not decisions made
#: here.
PLURAL_EXCEPTIONS = {
    ('Voice', 'Voices'): 'one vocal line vs the section that holds them',
}


def check_consistency(mapping, known):
    """Whole-map invariants, checked over every batch file at once.

    These are the rules the fix rounds enforce one at a time, kept here so
    that a later round cannot quietly break an earlier one.  `known` is the
    set of strings the English file actually contains.

    Hard failures:

    1. A value may not be empty, carry a control character or a U+FFFD, or
       have leading or trailing space.  An identity mapping is exempt from
       the space rule only because `build` exempts it, and `build` exempts it
       because a few source fields carry that space themselves (`<O. M. >`).

    2. Every key must be a string the English file actually contains, so a
       stale batch entry cannot pass unnoticed.

    3. A value may be shorter than its key only by a recognised plural
       ending.  `Basses` -> `Bass` and `Agogôs` -> `Agogô` lose `es` and `s`;
       `Charangos` -> `Charang` would lose `os` and is a mangling.

    Reported, not failed:

    4. Where a singular key exists, a translated plural takes the singular's
       wording - Vietnamese has no plural.  Identity mappings are exempt,
       because an English plural kept as English is not a disagreement, and
       `PLURAL_EXCEPTIONS` covers the pairs that genuinely differ.

    Returns a list of problem strings, empty when the map is clean.
    """
    problems = []
    for key, value in sorted(mapping.items()):
        if not value:
            continue
        if '\ufffd' in value:
            problems.append(f'U+FFFD: {key!r} -> {value!r}')
            continue
        bad = sorted({c for c in value if c in FORBIDDEN})
        if bad:
            problems.append(f'control character {[hex(ord(c)) for c in bad]}: '
                            f'{key!r} -> {value!r}')
            continue
        if value != value.strip() and value != key:
            problems.append(f'surrounding space: {key!r} -> {value!r}')
        if key not in known:
            problems.append(f'not in instrumentnames_en.xml: {key!r}')
            continue

        if value != key:
            if value.startswith(key):
                problems.append(f'value extends its key: {key!r} -> {value!r}')
            elif key.startswith(value) and key[len(value):] not in PLURAL_TAIL:
                problems.append(f'value drops a non-plural tail from its key: '
                                f'{key!r} -> {value!r}')

            if key.endswith('s'):
                sing = key[:-1]
                if sing in mapping and mapping[sing] not in (None, '') \
                        and mapping[sing] != value \
                        and (sing, key) not in PLURAL_EXCEPTIONS:
                    problems.append(
                        f'plural differs from its singular: {key!r} -> '
                        f'{value!r} but {sing!r} -> {mapping[sing]!r}')
    return problems
