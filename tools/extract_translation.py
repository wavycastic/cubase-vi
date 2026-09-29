#!/usr/bin/env python3
"""Extract the TRANSLATION.XML resource from a Steinberg PE and report on it.

    python tools/extract_translation.py <exe> [out.xml]

The UI string table is stored as plain, uncompressed UTF-8 XML in a PE
resource, which is what makes the whole approach possible: Cubase reads
<dir>/translation.xml from disk before falling back to the copy embedded in the
executable, so no binary patch is needed to change the language.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cubelib.pe import PE                       # noqa: E402

RESOURCE_NAME = 'TRANSLATION.XML'
OUT_DEFAULT = 'translation.xml'

if len(sys.argv) < 2:
    sys.exit(f'usage: extract_translation.py <exe> [{OUT_DEFAULT}]')

pe = PE(sys.argv[1])
res = pe.find_resource(RESOURCE_NAME)
if res is None:
    have = ', '.join(sorted({r.label for r in pe.resources()
                             if any(isinstance(p, str) for p in r.path)}))
    pe.close()
    sys.exit(f'{RESOURCE_NAME} resource not found in {sys.argv[1]}\n'
             f'named resources present: {have or "(none)"}')

xml = pe.bin.slice(res.off, res.size)
print(f'resource path: {res.label}')
print(f'resource at file 0x{res.off:X}, {res.size:,} bytes')
print(f'starts: {xml[:60]!r}')
print(f'ends  : {xml[-40:]!r}')

out = sys.argv[2] if len(sys.argv) > 2 else OUT_DEFAULT
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
    m = re.search(r'<String Key="' + re.escape(probe) + r'">\s*<us>([^<]*)</us>', text)
    print(f'  {probe:20} -> {"HIT: " + m.group(1) if m else "not found as exact key"}')

pe.close()
