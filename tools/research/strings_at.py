#!/usr/bin/env python3
import struct, sys, re

path = sys.argv[1]
raw = open(path, 'rb').read()
lo, hi = int(sys.argv[2], 16), int(sys.argv[3], 16)

seg = raw[lo:hi]
print(f'=== ASCII strings in 0x{lo:X}..0x{hi:X} (len {len(seg):,}) ===')
for m in re.finditer(rb'[\x20-\x7e]{4,}', seg):
    print(f'  +0x{m.start():05X} (abs 0x{lo+m.start():08X})  {m.group().decode()}')

print()
print('=== UTF-16LE strings ===')
for m in re.finditer(rb'(?:[\x20-\x7e]\x00){3,}', seg):
    try:
        s = m.group().decode('utf-16-le')
    except Exception:
        continue
    print(f'  +0x{m.start():05X} (abs 0x{lo+m.start():08X})  {s}')
