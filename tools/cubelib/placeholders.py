#!/usr/bin/env python3
"""Placeholder patterns, in one place.

Seven scripts in this project each compiled their own `PLACEHOLDER` regex, and
five of the seven were wrong in the same way:

    r'%(?:\\.\\d+)?[a-zA-Z%]'      # matches %s, %.3f
                                   # misses %1.0f  (positional)
                                   # misses %02d  (zero-padded)

`%1.0f` and `%02d` both occur in all_strings.tsv - twice and six times - and
`all_strings.tsv` reports both with **identical** placeholder lists, so the
rule "placeholders must match" passed on every one of them. It was not that
the strings were correct. It was that neither side of the comparison saw the
same placeholders.

That is the `[Ā-ỿ]` failure mode: a pattern that looks right and silently
matches nothing. AGENT.md §7 records nine tools that sat on that class for
seventeen rounds reporting zero findings every time.

    %s %d %i %.3f %.1f %.2f %.0f %02d %1.0f %l %%   and   {brace_form}

Note `%%` is a literal percent, not a placeholder, but it must still match:
a translation that drops one changes what the label prints.

    from cubelib.placeholders import PLACEHOLDER, placeholders

    if placeholders(src) != placeholders(val): ...
"""
import re

#: compiled; use `findall` for the multiset or `search` for presence
PLACEHOLDER = re.compile(
    r'%(?:\d+\$)?(?:\d+)?(?:\.\d+)?[a-zA-Z%]|\{[a-zA-Z0-9_]*\}')

#: every shape that actually occurs in keys/all_strings.tsv, with the count a
#: grep found. A new one appearing in the source means this list is stale.
SEEN_IN_SOURCE = {
    '%s': 606, '%d': 288, '%i': 38, '%.3f': 12, '%.1f': 10,
    '%.2f': 8, '%02d': 6, '%.0f': 4, '%1.0f': 2, '%l': 2,
}


def placeholders(s):
    """Return the sorted placeholder multiset of `s`.

    Sorted because a translation may legitimately reorder placeholders
    (`%1$s ... %2$s` -> `%2$s ... %1$s`); what must not change is the set.
    """
    return sorted(PLACEHOLDER.findall(s))


def missing(src, val):
    """Placeholders present in the source but absent from the translation."""
    have = set(placeholders(val))
    return [p for p in set(placeholders(src)) if p not in have]
