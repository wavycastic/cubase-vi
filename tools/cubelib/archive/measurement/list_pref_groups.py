#!/usr/bin/env python3
import re, sys
path = r'C:\Users\Administrator\AppData\Roaming\Steinberg\Cubase 15_64\Defaults.xml'
txt = open(path, encoding='utf-8', errors='replace').read()
groups = re.findall(r'<string name="Group" value="([^"]+)"', txt)
print(f'{len(groups)} groups\n')
for i in range(0, len(groups), 5):
    print('  ' + ' | '.join(f'{x[:26]:26}' for x in groups[i:i+5]))
print('\n--- GApplication members ---')
m = re.search(r'<string name="Group" value="GApplication"/>(.*?)\n      </item>', txt, re.S)
if m:
    for mm in re.finditer(r'<(\w+) name="([^"]+)"(?: value="([^"]*)")?\s*/>', m.group(1)):
        print(f'   {mm.group(1):10} {mm.group(2):36} = {mm.group(3) or ""}')
