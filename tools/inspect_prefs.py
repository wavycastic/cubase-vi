#!/usr/bin/env python3
"""Inspect Defaults.xml: list preference groups, hunt for the language setting."""
import re, sys, collections

path = sys.argv[1]
txt = open(path, encoding='utf-8', errors='replace').read()
print(f'{path}: {len(txt):,} chars')

groups = re.findall(r'<string name="Group" value="([^"]+)"', txt)
print(f'\nentries: {len(groups):,}   distinct groups: {len(set(groups)):,}')
interesting = [g for g in sorted(set(groups)) if re.search(r'gener|lang|locale|ui|app', g, re.I)]
print(f'groups matching gener/lang/locale/ui/app: {interesting[:40]}')

# look for a General group and dump its members
for g in set(groups):
    if g.lower() in ('general', 'preferencesgeneral', 'appgeneral'):
        print(f'\n--- dumping group {g!r} ---')
        m = re.search(r'<string name="Group" value="' + re.escape(g) + r'"/>(.*?)</item>', txt, re.S)
        if m:
            for mm in re.finditer(r'<(\w+) name="([^"]+)" value="([^"]*)"', m.group(1)):
                print(f'   {mm.group(1):8} {mm.group(2):32} = {mm.group(3)[:70]!r}')

print('\n--- any attribute or value mentioning lang/locale (case-insensitive) ---')
for m in re.finditer(r'<(\w+) name="([^"]*(?:[Ll]ang|[Ll]ocale)[^"]*)" value="([^"]*)"', txt):
    print(f'   {m.group(1):8} {m.group(2):32} = {m.group(3)[:60]!r}')

print('\n--- any attribute NAME mentioning lang/locale ---')
for m in re.finditer(r'name="([^"]*(?:[Ll]ang|[Ll]ocale)[^"]*)"', txt):
    print(f'   {m.group(1)!r}')
