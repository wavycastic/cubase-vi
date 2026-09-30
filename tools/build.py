#!/usr/bin/env python3
"""One-shot pipeline: extract -> merge -> build -> validate.

    python tools/build.py [path-to-Cubase15.exe]

Defaults to the usual install location. Everything is produced under keys/ and build/.
Nothing outside the repo is touched - use scripts/install.ps1 to deploy.
"""
import os, subprocess, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = lambda *p: os.path.join(ROOT, *p)
PY = sys.executable

EXE = sys.argv[1] if len(sys.argv) > 1 else r'E:\Steinberg\Cubase 15\Cubase15.exe'
BASE = T('keys', 'translation_original.xml')
TSV = T('keys', 'all_strings.tsv')
MAP = T('translations', 'vi.json')
OUT = T('build', 'translation_vi.xml')

os.makedirs(T('keys'), exist_ok=True)
os.makedirs(T('build'), exist_ok=True)

def run(args, title):
    print(f'\n=== {title} ===')
    r = subprocess.run([PY] + args, cwd=ROOT)
    if r.returncode != 0:
        print(f'!! {title} failed (exit {r.returncode})')
        sys.exit(r.returncode)

run([T('tools', 'extract_translation.py'), EXE, BASE], 'extract TRANSLATION.XML from exe')
run([T('tools', 'list_strings.py'), BASE, TSV], 'list all strings')
run([T('tools', 'merge_maps.py'), '--check'], 'check translation maps')
run([T('tools', 'prune_map.py'), '--dry-run'], 'check every map key exists in Cubase')
run([T('tools', 'check_style.py')], 'enforce hybrid style (AGENT.md)')
run([T('tools', 'check_punctuation.py')], 'check ? ! ; ... line breaks edge spaces')
run([T('tools', 'build_translation.py'), BASE, OUT, MAP], 'build Vietnamese translation.xml')
run([T('tools', 'validate_translation.py'), OUT], 'validate output')

print(f'\nDone. -> {os.path.relpath(OUT, ROOT)}  ({os.path.getsize(OUT):,} bytes)')
print('Deploy with:  powershell -File scripts\\install.ps1 -Action install')
