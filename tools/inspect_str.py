#!/usr/bin/env python3
"""Query original languages and VI for strings matching a pattern or domain.

Usage:
    python tools/inspect_str.py <query>
"""
import sys, re, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
orig_xml = open(os.path.join(ROOT, 'keys', 'translation_original.xml'), encoding='utf-8').read()
vi = json.load(open(os.path.join(ROOT, 'translations', 'vi.json'), encoding='utf-8'))

q = sys.argv[1] if len(sys.argv) > 1 else ''

pat = re.compile(r'<String Key="([^"]*' + re.escape(q) + r'[^"]*)">(.*?)</String>', re.S | re.IGNORECASE)

matches = list(pat.finditer(orig_xml))
print(f"Found {len(matches)} matching keys for '{q}':\n")
for m in matches[:30]:
    k = m.group(1)
    body = m.group(2)
    langs = dict(re.findall(r'<(\w+)>(.*?)</\1>', body, re.S))
    print(f"KEY: {k}")
    print(f" US: {langs.get('us', '')}")
    print(f" DE: {langs.get('de', '')}")
    print(f" FR: {langs.get('fr', '')}")
    print(f" VI: {vi.get(k, '<MISSING>')}")
    print("-" * 50)
