# Commit Convention

All commits in English. No Vietnamese prose in subject or body.
Vietnamese appears only inside quoted data (translation examples).

## Subject

- One line, max 100 chars, no trailing period.
- Round work: `round NNN: <what> (<count> strings, <scope>)`
- Docs: `docs: <what>`, tooling: `feat: <what>` / `fix: <what>`
- Keep domain terms exactly as in the map: `Time Signature`, not
  "time signature"; `giu EN` never appears, write `keep in English`.

Good:

- `round 222: fix 5 strings (Still/Pause RS422, Absolute Mode)`
- `round 146: keep Staff in English in Score Editor (35 strings)`
- `AGENT.md compressed: 972 -> 547 lines (79KB -> 43KB, down 46%)`

Bad:

- `round 222: sua 5 chuoi` (Vietnamese)
- `round 222: fix 5 confusing strings.` (trailing period)
- `stuff` (no scope, no count)

## Body (optional, for rounds with findings)

- Numbered list, one item per defect class or decision.
- Each item: cause, evidence (DE/FR/ES counts, sibling strings),
  then the fix. Evidence before conclusion.
- Before→after pairs stay verbatim, quotes included:
  `'All clips in editor are used.' -> 'Dung tat ca Clip trong Editor.'`
- End with the pipeline line when it ran:
  `Pipeline section 9: 88 batches, style PASS, punct 0, 174 tests PASS.`

## Never

- Vietnamese prose outside quotes. `chuoi`, `sua`, `dong bo`,
  `khong the`, `do truoc` have English forms; use them.
- Shell artifacts in the message: no literal backslashes,
  no `\n` text, no pasted terminal escape codes.
- `git commit -m` with smart quotes or unescaped `$`, backticks.

## Rewriting history

- Message-only rewrite: `git filter-branch --msg-filter`, then
  compare `HEAD^{tree}` before/after (must be identical), count
  commits (must be unchanged), then `git push --force`.
- Keep a local backup branch until the push is verified.
