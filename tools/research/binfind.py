#!/usr/bin/env python3
"""Search a binary file for ASCII / UTF-16LE / UTF-16BE / UTF-8 occurrences of a pattern."""
import sys, argparse, mmap, re

def encodings(s):
    return {
        'utf8':    s.encode('utf-8'),
        'ascii':   s.encode('latin-1', 'ignore'),
        'utf16le': s.encode('utf-16-le'),
        'utf16be': s.encode('utf-16-be'),
    }

def printable(b, lo=32, hi=126):
    return all(lo <= c < hi or c in (9, 10, 13) for c in b)

def dump(mm, start, back=48, fwd=160):
    s = max(0, start - back)
    e = min(len(mm), start + fwd)
    chunk = mm[s:e]
    out = []
    for c in chunk:
        if 32 <= c < 127:
            out.append(chr(c))
        else:
            out.append('\ufffd' if c > 255 else '.')
    return s, ''.join(out)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('file')
    ap.add_argument('pattern')
    ap.add_argument('-n', '--max', type=int, default=20)
    ap.add_argument('-c', '--context', type=int, default=160)
    a = ap.parse_args()

    with open(a.file, 'rb') as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        for name, pat in encodings(a.pattern).items():
            if not pat:
                continue
            hits = []
            pos = 0
            while len(hits) < a.max:
                i = mm.find(pat, pos)
                if i < 0:
                    break
                hits.append(i)
                pos = i + 1
            if not hits:
                continue
            print(f'=== {name}  ({len(hits)} hit(s), showing <= {a.max}) ===')
            for i in hits:
                off, txt = dump(mm, i, a.context // 2, a.context // 2)
                mark = i - off
                print(f'  @0x{i:08X} (dec {i})')
                print('   ', txt.replace('\ufffd', '\u00b7'))
        mm.close()

if __name__ == '__main__':
    main()
