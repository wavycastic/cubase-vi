#!/usr/bin/env python3
"""Note-value family: one rendering per duration.

AGENT.md 2 keeps "Note" in English, so every duration reads "Note 1/8", never
"1/8 Note" and never "Nốt 1/8".

Two defects the earlier passes left:
  * the order was inconsistent - "1/8 Note" and "Note 1/8" for the same thing
  * the bracketed note name was dropped entirely, so "1/8 Note (Quaver)" became
    "1/8 Note" and the settings no longer said which note type it meant

The name is kept, in Vietnamese, inside the brackets the key already had.
"""

WORDING = {
    # --- bare durations -----------------------------------------------------
    '1/2 Note': 'Note 1/2',
    '1/4 Note': 'Note 1/4',
    '1/8 Note': 'Note 1/8',
    '1/16 Note': 'Note 1/16',
    '1/32 Note': 'Note 1/32',
    '1/64 Note': 'Note 1/64',
    '1/128 Note': 'Note 1/128',
    '1/256 Note': 'Note 1/256',
    '1/512 Note': 'Note 1/512',

    # --- durations that name the note type ----------------------------------
    '1/2 Note (Minim)': 'Note 1/2, nốt bán',
    '1/4 Note (Crotchet)': 'Note 1/4, nốt cường',
    '1/8 Note (Quaver)': 'Note 1/8, nốt móc đơn',
    '1/16 Note (Semiquaver)': 'Note 1/16, nốt móc kép',
    '1/32 Note (Demisemiquaver)': 'Note 1/32, nốt móc ba',
    '1/64 Note (Hemidemisemiquaver)': 'Note 1/64, nốt móc tư',

    # --- the "Nốt ..." spellings the earlier pass introduced -----------------
    '1/16 Notes (Semiquavers) in 1/8 Note (Quaver) Denominator Time '
    'Signatures':
        'Note 1/16, nốt móc kép, trong số chỉ nhịp mẫu số Note 1/8, nốt móc đơn',
    '1/32 Notes (Demisemiquavers) in 1/16 Note (Semiquaver) Denominator Time '
    'Signatures':
        'Note 1/32, nốt móc ba, trong số chỉ nhịp mẫu số Note 1/16, nốt móc kép',
    '1/8 Notes (Quavers) in 1/4 Note (Crotchet) Denominator Time Signatures':
        'Note 1/8, nốt móc đơn, trong số chỉ nhịp mẫu số Note 1/4, nốt cường',
    '1/8 Notes (Quavers) in Simple Time Signatures With a Half-Bar':
        'Note 1/8, nốt móc đơn, trong số chỉ nhịp đơn có nửa Bar',
    'Rests Within Groups of 1/8 Notes (Quavers) in Simple Time Signatures '
    'With a Half-Bar':
        'Dấu lặng trong nhóm Note 1/8, nốt móc đơn, ở số chỉ nhịp đơn có nửa Bar',
    '1/8 Note (Quaver) Beams When Adjacent Tuplet Starts or Ends With an 1/8 '
    'Note':
        'Đuôi nốt của Note 1/8, nốt móc đơn, khi liên nhịp liền kề bắt đầu '
        'hoặc kết thúc bằng Note 1/8',
    'Groups of Notes in Long Time Signatures With a Half-Bar':
        'Nhóm nốt trong số chỉ nhịp dài có nửa Bar',
    'Groups of Notes in Simple Time Signatures With a Half-Bar':
        'Nhóm nốt trong số chỉ nhịp đơn có nửa Bar',
    # --- note durations with no denominator ------------------------------
    # AGENT.md section 4: the note-duration fields keep "Note" in English and
    # read "Note 1/8". These four keys were left as "Moc 16", which is the
    # order reversed - the same defect as 163 other strings, but in a value too
    # short for fix_word_order.py to match on.
    '8th': 'Note 1/8',
    '16th': 'Note 1/16',
    '32th': 'Note 1/32',
    '64th': 'Note 1/64',
}
