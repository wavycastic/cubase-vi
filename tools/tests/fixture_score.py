"""A synthetic `instrumentnames_XX.xml`, faithful in the ways that matter.

`cubelib.score` edits the file by splicing text rather than re-serialising
XML, because the shipped files are not round-trippable through ElementTree
without changing bytes the engine does not care about but a diff would.  That
decision is only safe if the tests exercise the quirks that forced it, so this
fixture carries all of them deliberately:

  * CRLF line endings, a `<?xml version="1.0" ?>` header with a space before
    the `?>`, and tab indentation;
  * `<parentEntityID/>` and `<customVariantString/>` written self-closing with
    no space before the slash, while `<data>` children are not;
  * an entity whose children are in a different order from the rest
    (`<name>` before `<entityID>`, `<customVariantString/>` wedged into the
    middle of `<data>`);
  * XML escapes inside a value, to prove an untouched field keeps them;
  * a value with a trailing space, which `build` must allow as an identity
    mapping and reject as a translation;
  * an empty name field, written as `<pluralShortName/>`;
  * a plural form that differs from the singular, and a short name shared by
    both, which is what makes the plural slot worth having.

Written by hand rather than generated, so that a test failure points at a
specific shape instead of at a generator that got it wrong.
"""
import os

HEADER = ('<?xml version="1.0" ?>\r\n'
          '<kScoreLibrary>\r\n'
          '\t<instrumentNames>\r\n'
          '\t\t<language>kEnglish</language>\r\n'
          '\t\t<entities array="true">\r\n'
          '\t\t\t')
FOOTER = ('\t\t\t</entities>\r\n'
          '\t\t</instrumentNames>\r\n'
          '</kScoreLibrary>\r\n')


def entity(eid, name, *, ui=None, short=None, plural=None,
           plural_short=None, first=False, extra='', language='kEnglish'):
    """One entity block, at the indentation the shipped file uses.

    `first=True` reproduces the aluphone quirk: a complete `<name>` element
    before `<entityID>` rather than after it.
    """
    ui = name if ui is None else ui
    short = '' if short is None else short
    plural = ui if plural is None else plural
    plural_short = short if plural_short is None else plural_short
    name_line = f'\t\t\t\t<name>{name}</name>\r\n'
    before, after = (name_line, '') if first else ('', name_line)
    return (
        '<InstrumentNameEntityDefinition>\r\n'
        + before
        + f'\t\t\t\t<entityID>{eid}</entityID>\r\n'
        + after
        + '\t\t\t\t<parentEntityID/>\r\n'
        '\t\t\t\t<inheritanceMask>0</inheritanceMask>\r\n'
        '\t\t\t\t<data>\r\n'
        f'\t\t\t\t\t<uiName>{ui}</uiName>\r\n'
        + extra
        + f'\t\t\t\t\t<singularFullName>{ui}</singularFullName>\r\n'
        + (f'\t\t\t\t\t<singularShortName>{short}</singularShortName>\r\n'
           if short else '\t\t\t\t\t<singularShortName/>\r\n')
        + f'\t\t\t\t\t<pluralFullName>{plural}</pluralFullName>\r\n'
        + (f'\t\t\t\t\t<pluralShortName>{plural_short}</pluralShortName>\r\n'
           if plural_short else '\t\t\t\t\t<pluralShortName/>\r\n')
        + '\t\t\t\t\t<gender>kNeutral</gender>\r\n'
        + f'\t\t\t\t\t<language>{language}</language>\r\n'
        + '\t\t\t\t</data>\r\n'
        '</InstrumentNameEntityDefinition>\r\n'
        '\t\t\t')


DOCUMENT = HEADER + ''.join([
    # A share reused by a second entity, so `source_strings` has to report
    # more than one user for it.
    entity('instrumentname.keyboard.accordion', 'Accordion',
           short='Accord.', plural='Accordions'),
    entity('instrumentname.keyboard.piano', 'Piano', short='Pno',
           plural='Pianos'),
    # An empty short name and an empty plural short name.
    entity('instrumentname.latin.unpitched.cajon', 'Cajon',
           short=None, plural_short=None),
    # A trailing space in a value - legal in the source, illegal in a
    # translation.
    entity('instrumentname.keyboard.ondes', 'Ondes Martenot ',
           short='O. M. ', plural='Ondes Martenots '),
    # XML escapes, to prove an untouched field keeps them byte for byte.
    entity('instrumentname.strings.bass', 'Bass &amp; Violin',
           short='B&amp;V', plural='Basses &amp; Violins'),
    # The odd one out: <name> before <entityID>, <customVariantString/> inside
    # <data>, and - as in all eight non-English catalogues Steinberg ships -
    # a language marker that was never retagged.
    entity('instrumentname.pitchedpercussion.aluphone', 'Aluphone',
           short='Alu.', plural='Aluphones', first=True,
           extra='\t\t\t\t\t<customVariantString/>\r\n',
           language='kEnglish'),
]) + FOOTER

#: What `DOCUMENT` contains, as the tests want to state it.
ENTITIES = 6
LANGUAGE_MARKERS = 1 + ENTITIES
