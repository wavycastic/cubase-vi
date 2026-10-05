# Provenance / Copyright

## What this repo contains

| Path | Origin | Licence |
|---|---|---|
| `translations/**` | written for this repo | MIT, see `LICENSE` |
| `tools/**`, `scripts/**`, `docs/**`, `README.md` | written for this repo | MIT, see `LICENSE` |
| `keys/all_strings.tsv` | **extracted from `Cubase15.exe`** | © Steinberg Media Technologies GmbH |

## `keys/all_strings.tsv`

This file is a plain-text dump of the 10,737 user-interface string keys and their
English (`us`) values, taken from the `TRANSLATION.XML` resource inside
`Cubase15.exe` of Cubase 15.0.30. It is **Steinberg's content**, not this
project's, and it is committed here purely as a **reference table** so that
people can look up what needs translating and contribute entries.

It is committed deliberately and is expected to change rarely — regenerate it
when you move to a new Cubase version:

```powershell
python tools\build.py "E:\Steinberg\Cubase 15\Cubase15.exe"
```

The original `keys\translation_original.xml` (4.65 MB, all 9 of Steinberg's own
translations) is **not** committed; `tools/build.py` regenerates it from your
own Cubase installation.

## Scope

Cubase, its interface strings and all bundled content are trademarks and
copyright of Steinberg. This project does not redistribute the application,
does not alter it, and does not touch its licensing. It only provides a
Vietnamese translation of the interface for use with a Cubase installation you
already own and have licensed.

If you are not the owner of a Cubase licence, do not use this.

Steinberg has published localisations of Cubase into nine languages (English,
German, French, Spanish, Italian, Portuguese, Japanese, Chinese, Russian). If
Steinberg ever ships an official Vietnamese localisation, use that instead —
it will be better than any community translation.
