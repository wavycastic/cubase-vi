"""Measure what each language costs in translation.xml, and what dropping six
of them would actually save.

    python tools/measure_languages.py
"""
import re, collections, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for name in ('keys/translation_original.xml', 'build/translation_vi.xml'):
    p = os.path.join(ROOT, name.replace('/', os.sep))
    x = open(p, encoding='utf-8').read()
    bodies = re.findall(r'<String Key="[^"]*">(.*?)</String>', x, re.S)
    tot = collections.Counter()
    n = collections.Counter()
    for b in bodies:
        for lang, val in re.findall(r'<(\w+)>(.*?)</\1>', b, re.S):
            # the bytes the element costs: the tag, the text, the closing tag
            tot[lang] += len(val.encode('utf-8')) + 2 * len(lang) + 7
            n[lang] += 1
    T = sum(tot.values())
    size = os.path.getsize(p)
    print(f'=== {name}')
    print(f'    file {size:,} bytes, {len(bodies):,} String entries')
    print(f'    {"lang":<6}{"entries":>9}{"bytes":>12}{"share":>8}')
    for lang, c in tot.most_common():
        print(f'    {lang:<6}{n[lang]:>9,}{c:>12,}{100 * c / T:>7.1f}%')
    print(f'    {"all":<6}{sum(n.values()):>9,}{T:>12,}')
    keep = tot['us'] + tot.get('vi', 0)
    print(f'    us + vi would be {keep:,} = {100 * keep / T:.1f}% of the text')
    print(f'    estimated file after dropping the other six: '
          f'~{size - (T - keep):,} bytes')
    print()
