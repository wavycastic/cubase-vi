#!/usr/bin/env python3
"""Read and patch colours in a Steinberg skin file (`Skins/*.srf`).

    python tools/skin_edit.py list  skin.srf --grep wave
    python tools/skin_edit.py get   skin.srf eventWaveMuted
    python tools/skin_edit.py set   skin.srf -o fl-wave.srf eventWaveMuted="$210,005,200"

Why this is safe to write back
------------------------------
The container is flat: a header, then 842 members, each one preceded by the
leftover name `/Thumbs.db\r\n`, then a lookup table.  Members are either a raw
PNG or a zlib stream.  Nothing is encrypted and there is no checksum over the
file, so the way to keep a patched skin honest is:

  * re-emit every member we did **not** touch byte for byte, so only the patched
    members can shift the offsets of what follows;
  * re-parse our own output with the same reader and compare every payload.

The trailing table (49,865 bytes at 0x134DF87) is a *git export manifest* - it
lists 892 entries including `.gitignore`, `audio` and `..`, i.e. files that are
not members at all - so it is copied through untouched.  Whether Cubase reads it
at runtime is **not verified**; `--check-index` reports how far the recorded
offsets drift after a patch so the question can be settled by testing.
"""
import argparse
import re
import sys
import zlib

COLOR = re.compile(
    rb'<color\s+name="([^"]+)"(\s+[^>]*?)?value="([^"]*)"', re.I)
TEMPLATE = re.compile(rb'<template\s+name="([^"]+)"', re.I)
MAGIC = b'Steinberg Resource File'
LEFTOVER = b'/Thumbs.db\r\n'


def load(path):
    """Return (raw, header, members, trailing).

    `members` entries are (kind, payload, stored, sep) where `sep` is the raw
    bytes that sit between the previous member and this one.  The packer only
    writes `/Thumbs.db\r\n` before *some* members - the 842 members need 10.104
    separator bytes on a full re-pack but the shipped file has far fewer - so the
    separators are copied through verbatim rather than regenerated.  That is what
    makes an unchanged re-pack byte-identical to the input.
    """
    data = open(path, 'rb').read()
    if not data.startswith(MAGIC):
        raise SystemExit(f'{path}: not a Steinberg Resource File')
    first = data.find(LEFTOVER)
    if first < 0:
        raise SystemExit(f'{path}: no members found')
    header = data[:first]                 # magic + CRLF, kept verbatim
    members = []
    pos = first
    while pos < len(data):
        mark = pos
        if data[pos:pos + len(LEFTOVER)] == LEFTOVER:
            pos += len(LEFTOVER)
            if pos >= len(data):
                members.append(None)      # trailing separator, keep in trailing
                pos = len(data)
                break
        if data[pos:pos + 4] == b'\x89PNG':
            end = data.find(b'IEND', pos)
            if end < 0:
                break
            end += 8
            members.append(('png', data[pos:end], data[pos:end],
                            data[mark:pos]))
            pos = end
        elif data[pos:pos + 1] == b'\x78':
            try:
                do = zlib.decompressobj()
                payload = do.decompress(data[pos:])
            except zlib.error:
                break
            used = len(data) - pos - len(do.unused_data)
            kind = 'skin' if payload.lstrip(
                b'\xef\xbb\xbf \t\r\n')[:5] == b'<skin' else 'xml'
            members.append((kind, payload, data[pos:pos + used],
                            data[mark:pos]))
            pos += used
        else:
            break
    return data, header, members, data[pos:]


def is_text(payload):
    head = payload.lstrip(b'\xef\xbb\xbf \t\r\n')
    return head[:1] == b'<'


def cmd_list(a):
    _, _, members, _ = load(a.srf)
    rx = re.compile(a.grep, re.I) if a.grep else None
    shown = 0
    for i, m4 in enumerate(members):
        if m4 is None:
            continue
        kind, payload = m4[0], m4[1]
        if kind not in ('xml', 'skin') or not is_text(payload):
            continue
        for m in COLOR.finditer(payload):
            name = m.group(1).decode('utf-8', 'replace')
            if rx and not rx.search(name):
                continue
            print(f'#{i:<4} {name:<32} = {m.group(3).decode("utf-8", "replace")}')
            shown += 1
        if a.grep:
            for m in TEMPLATE.finditer(payload):
                name = m.group(1).decode('utf-8', 'replace')
                if rx.search(name):
                    print(f'#{i:<4} [template] {name}')
                    shown += 1
    print(f'\n{shown} matching entr(y|ies) in {a.srf}')


def cmd_get(a):
    _, _, members, _ = load(a.srf)
    for m4 in members:
        if m4 is None or m4[0] not in ('xml', 'skin') or not is_text(m4[1]):
            continue
        for m in COLOR.finditer(m4[1]):
            if m.group(1).decode('utf-8', 'replace') == a.name:
                print(m.group(3).decode('utf-8', 'replace'))
                return
    raise SystemExit(f'no colour named {a.name!r}')


def patch_payload(payload, changes):
    """Apply name=value edits to one XML member.

    Returns (new_payload, [names actually changed]).
    """
    wanted = {k: v.encode('utf-8') for k, v in changes.items()}
    hits = []

    def repl(m):
        name = m.group(1).decode('utf-8', 'replace')
        if name not in wanted:
            return m.group(0)
        hits.append(name)
        return m.group(0)[:m.start(3) - m.start(0)] + wanted[name] + b'"'

    return COLOR.sub(repl, payload), hits


def compress_to(payload, target):
    """zlib-compress `payload` to exactly `target` bytes, or None.

    A patch that changes the compressed length shifts every member after it, and
    the trailing lookup table then records offsets that are out of date.  That
    table may well be read at run time - nobody has verified - so the cheap way
    to remove the whole question is to make the patch **length preserving**: pad
    the payload with insignificant XML whitespace until deflate lands on exactly
    the original stored size.

    Returns None when no padding in `MAX_PAD` bytes reaches the target, which
    means the edit genuinely changed the compressed size and the caller has to
    decide whether that is acceptable.
    """
    level = 9
    for pad in range(MAX_PAD + 1):
        blob = zlib.compress(payload + (b' ' * pad), level)
        if len(blob) == target:
            return blob
        if len(blob) > target and pad:
            return None            # overshot: more padding only grows it
    return None


MAX_PAD = 4096


def cmd_set(a):
    changes = {}
    for item in a.assign:
        if '=' not in item:
            raise SystemExit(f'expected name=value, got {item!r}')
        k, v = item.split('=', 1)
        changes[k] = v
    data, header, members, trailing = load(a.srf)

    out = bytearray(header)
    changed = []
    for i, m4 in enumerate(members):
        if m4 is None:
            continue
        kind, payload, stored, sep = m4
        if kind in ('xml', 'skin') and is_text(payload):
            new, hits = patch_payload(payload, changes)
            if hits:
                blob = None
                if a.keep_size:
                    blob = compress_to(new, len(stored))
                    if blob is None:
                        raise SystemExit(
                            f'--keep-size: khong ninh khong cua member #{i} ve '
                            f'{len(stored)} byte (ban goc {len(payload):,} byte '
                            f'payload). Cau lenh nay bao dam moi gia tri da doi '
                            f'seu lech het so byte, nen dung khi muon ghi de '
                            f'truc tiep skin.srf.')
                if blob is None:
                    blob = zlib.compress(new, 9)
                out += sep + blob
                changed.append((i, hits, len(stored), len(blob)))
                continue
        out += sep + stored
    out += trailing

    missing = set(changes)
    for _i, hits, _old, _new in changed:
        missing -= set(hits)
    if missing:
        raise SystemExit('no such colour(s): ' + ', '.join(sorted(missing)))

    with open(a.out, 'wb') as fh:
        fh.write(out)

    print(f'wrote {a.out}: {len(out):,} bytes (was {len(data):,})')
    for i, hits, old, new in changed:
        print(f'  member #{i}: {", ".join(hits)}  stored {old:,} -> {new:,} '
              f'({new - old:+,})')
    if not changed:
        print('  (nothing matched - output is a copy)')

    # self-check: re-parse our own output and compare every payload
    _d2, _h2, members2, trailing2 = load(a.out)
    if len(members2) != len(members):
        raise SystemExit(f'FAIL: member count {len(members)} -> {len(members2)}')
    touched = [c[0] for c in changed]
    for i, m4 in enumerate(members):
        if m4 is None:
            continue
        k1, p1 = m4[0], m4[1]
        k2, p2 = members2[i][0], members2[i][1]
        if k1 != k2:
            raise SystemExit(f'FAIL: member {i} kind {k1} -> {k2}')
        if p1 != p2 and i not in touched:
            raise SystemExit(f'FAIL: member {i} payload changed unexpectedly')
    if trailing2 != trailing:
        raise SystemExit('FAIL: trailing table changed')
    print(f'  self-check ok: {len(members2)} members, payloads intact')

    if a.check_index:
        end = len(out) - len(trailing)
        was = len(data) - len(trailing)
        delta = sum(c[3] - c[2] for c in changed)
        print(f'  members now occupy 0x0..0x{end:X} (was 0x{was:X}); '
              f'trailing table copied verbatim ({len(trailing):,} bytes), so '
              f'its recorded offsets are {delta:+,} bytes out of date')


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)

    p = sub.add_parser('list')
    p.add_argument('srf')
    p.add_argument('--grep')
    p.set_defaults(func=cmd_list)

    p = sub.add_parser('get')
    p.add_argument('srf')
    p.add_argument('name')
    p.set_defaults(func=cmd_get)

    p = sub.add_parser('set')
    p.add_argument('srf')
    p.add_argument('-o', '--out', required=True)
    p.add_argument('--check-index', action='store_true',
                   help='report where the members end after patching')
    p.add_argument('--keep-size', action='store_true',
                   help='fail unless every patched member compresses back to '
                        'its original byte count, so no offset in the trailing '
                        'table goes stale (pads the payload with XML whitespace '
                        'to hit the size exactly)')
    p.add_argument('assign', nargs='+', metavar='name=value')
    p.set_defaults(func=cmd_set)

    a = ap.parse_args()
    return a.func(a) or 0


if __name__ == '__main__':
    sys.exit(main())
