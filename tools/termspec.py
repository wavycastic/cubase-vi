#!/usr/bin/env python3
"""Boc terms_do_not_translate.json thanh luat.

Hai loai mau:

    "Track": ["\\brãnh\\b"]                     sai o moi ngu canh
    "Bypass": [{"vi": "\\bbỏ qua\\b",
                "src": "\\bbypass\\b"}]          chi sai khi NGUON khop src

Loai thu hai khong phai chuyen phuc tap hoa. `Bypass -> bo qua` la sai
(13 chuoi da sua o dot 72), nhung `Ignore -> bo qua` la dung va co 23
chuoi nhu vay trong ban dich. Mot mau vo dieu kien se chan het 23 chuoi
dung do, va mot bo do bao dong gia thi khong ai doc nua (AGENT.md §7).

API:

    from termspec import rules_for_style, rules_for_tests

    for rx_src, rx_vi, term in rules_for_style():
        if rx_src is None or rx_src.search(src):      # None = moi ngu canh
            if rx_vi.search(val): ...

`rules_for_tests()` chi tra mau vo dieu kien - do la mau co the test hai
chieu ma khong can nguon.

Sinh tu: tools/tests/fixture_translation.py (load) va check_style.py.
"""
import json
import os
import re

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPEC = os.path.join(_ROOT, 'terms_do_not_translate.json')


def spec():
    return json.load(open(SPEC, encoding='utf-8'))


def _compile(p):
    if isinstance(p, str):
        return None, re.compile(p, re.I)
    return re.compile(p['src'], re.I), re.compile(p['vi'], re.I)


def rules_for_style():
    """[(rx_src | None, rx_vi, term)] - rx_src None nghia la moi ngu canh."""
    out = []
    for term, pats in spec()['forbidden'].items():
        if term.startswith('_'):
            continue
        for p in pats:
            rx_src, rx_vi = _compile(p)
            out.append((rx_src, rx_vi, term))
    return out


def rules_for_tests():
    """[(term, compiled_vi)] - chi mau vo dieu kien, test duoc doc lap."""
    out = []
    for term, pats in spec()['forbidden'].items():
        if term.startswith('_'):
            continue
        for p in pats:
            if isinstance(p, str):
                out.append((term, re.compile(p, re.I)))
    return out


def check(src_text, val):
    """[(term, matched_text)] - cac luat bi vi pham boi (src, val)."""
    hits = []
    for rx_src, rx_vi, term in rules_for_style():
        if rx_src is not None and not rx_src.search(src_text):
            continue
        m = rx_vi.search(val)
        if m:
            hits.append((term, m.group(0)))
    return hits