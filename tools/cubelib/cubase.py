"""Cubase-specific knowledge: where things live and what is worth knowing.

Kept apart from the format parsers in `binary`/`pe`/`qm`/`srf` so those stay
reusable for any Steinberg binary, not just a particular Cubase build.
"""
import os

DEFAULT_INSTALL = os.environ.get('CUBASE_DIR', r'E:\Steinberg\Cubase 15')

# Steinberg UI languages in the order the translation.xml LanguageTable uses.
# The Scoring Engine's own enum is much larger; see RESEARCH.md.
UI_LANGUAGES = ['us', 'de', 'fr', 'es', 'it', 'pt', 'jp', 'zh', 'ru']
LANG_NAMES = {'us': 'English', 'de': 'German', 'fr': 'French', 'es': 'Spanish',
              'it': 'Italian', 'pt': 'Portuguese', 'jp': 'Japanese',
              'zh': 'Chinese', 'ru': 'Russian'}

TARGET_LANG = 'vi'
TARGET_LANG_NAME = 'Vietnamese'

# RCDATA payloads embedded in Cubase15.exe.  TRANSLATION.XML is the one with a
# documented on-disk override path; the rest would need a PE patch.
EXE_RESOURCES = [
    'TRANSLATION.XML', 'TYPELIST.XML', 'STYLELIST.XML', 'CHARACTERLIST.XML',
    'POSTCATEGORYLIST.XML', 'APPLICATIONTYPELIST.XML', 'TEMPLATECATEGORYLIST.XML',
    'SOUNDCOMPONENTLIST.XML', 'PROPERTYLIST.XML', 'MOODLIST.XML',
    'ARTICULATIONLIST.XML', 'VOICINGS-BASIC.XML', 'VOICINGS-PIANO.XML',
    'VOICINGS-GUITAR.XML', 'NAMINGSCHEMEDEFAULTS.XML', 'TRACKCONTROLSDEFAULT.XML',
]

# Scoring Engine (the Dorico engine embedded in Cubase) localisation.
SCORING_L10N = os.path.join('Components', 'ScoringEngine', 'l10n')
SCORING_INSTRUMENT_FILES = 624     # InstrumentNameEntityDefinition per language


class Install:
    """Resolved paths inside a Cubase installation."""

    def __init__(self, root=DEFAULT_INSTALL):
        self.root = root

    def __repr__(self):
        return f'<Cubase install {self.root!r}>'

    def path(self, *parts):
        return os.path.join(self.root, *parts)

    @property
    def exists(self):
        return os.path.isdir(self.root)

    @property
    def exe(self):
        return self.path('Cubase15.exe')

    @property
    def scoring_engine(self):
        return self.path('Components', 'ScoringEngine', 'ScoringEngine.dll')

    @property
    def scoring_l10n(self):
        return self.path('Components', 'ScoringEngine', 'l10n')

    @property
    def skin(self):
        return self.path('Skins', 'skin.srf')

    @property
    def translation_xml(self):
        return self.path('translation.xml')

    def instrument_names(self, suffix='en'):
        return os.path.join(self.scoring_l10n, f'instrumentnames_{suffix}.xml')

    def catalogue(self, suffix='en'):
        return os.path.join(self.scoring_l10n, f'strings_{suffix}.qm')

    def describe(self):
        rows = [f'install: {self.root}' + ('' if self.exists else '   (NOT FOUND)')]
        for label, p in (('exe', self.exe), ('scoring engine', self.scoring_engine),
                         ('scoring l10n', self.scoring_l10n), ('skin', self.skin),
                         ('translation.xml', self.translation_xml)):
            mark = 'ok' if os.path.exists(p) else '-'
            size = f'{os.path.getsize(p):,}' if os.path.exists(p) else ''
            rows.append(f'  [{mark:>2}] {label:18} {p}  {size}')
        return '\n'.join(rows)
