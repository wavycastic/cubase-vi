#!/usr/bin/env python3
"""Chia 10.737 chuoi thanh vung de dich tiep cho de.

Vung cu (sample_domain.py) bat 8 cum tu trong key. Do la 68% chuoi khong
khop vung nao, va 3 cach tach general da thu deu danh het ve mot cho. Ly do:
key Cubase la chuoi UI tieng Anh khong co tien to, nen phai phan loai theo
NOI DUNG, va phep do phai rong hon.

Dung 3 lop, thu tu tu quan trong den chung nhat:

  1. MIEN   - tu khoa ro nhat: Warp, Dynamics, Clef, SysEx, Timecode...
  2. LOAI   - hinh thuc: nhan / cau lenh / van xuoi / cau hoi
  3. CHI MUC con lai - de khong co nhom nao rong hon 3.000 chuoi

Moi vung in so chuoi + ty le. `general` con lai phai lon hon 3.000 thi bao
"vung nay con qua lon" thay vi im lang de ban tu tin la vung.

    python tools\\by_region.py              # bang tong hop
    python tools\\by_region.py --region mixer
"""
import json, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = lambda *p: os.path.join(ROOT, *p)

vi = json.load(open(T('translations', 'vi.json'), encoding='utf-8'))
src = {}
for line in open(T('keys', 'all_strings.tsv'),
                 encoding='utf-8').read().splitlines()[1:]:
    if '\t' in line:
        k, u = line.split('\t', 1)
        src[k] = u

# (ten vung, regex) - thu tu la thu tu UUU TIEN, dung dau bang vung roi
REGIONS = [
    # ---- MIDI / phan cung ----
    ('midi', r'\b(midi|sysex|sys ex|cc mode|cc:|nrpn|rpn|mpe|mtc|omni|'
             r'pitch ?bend|aftertouch|poly pressure|velocity|controller|'
             r'mapping|learn|assign|remote|surface|9.?pin|din|thru|merge|'
             r'quantize|transpose|transpose ?instrument|automation|'
             r'pitch|velocity|modulation|expression)\b'),
    # ---- ban nhac / xuong nhac ----
    ('notation', r'\b(clef|clefs|staff|stave|ledger|beam|beaming|slur|tie|'
                 r'tuplet|note ?head|notehead|noteheads|rest|rests|system|'
                 r'bar ?line|accidental|rhythm|pedal|bowing|fingering|'
                 r'drum|drums|score|conductor|lyrics|sylabi|coda|segno|'
                 r'ottava|caesura|breath|fermata|grace ?note|up ?stem|'
                 r'down ?stem|chord|harmony|voicing|tension|articulation|'
                 r'scale|major|minor|diminished|dominant|seventh|ninth|'
                 r'key ?signature|time ?signature|sharp|flat|natural)\b'),
    # ---- audio / trinh duyet ----
    ('audio', r'\b(warp|audio|waveform|wave|sample rate|bit depth|bit|'
              r'latency|buffer|asio|driver|device|fade|crossfade|fade ?in|'
              r'fade ?out|freeze|varioaudio|vari ?audio|transient|formant|'
              r'pitch ?shift|loop|clip|event|part|pool|slice|chop|'
              r'multi.?beat|elastic|audio ?warp)\b'),
    # ---- tron am ----
    ('mixing', r'\b(insert|send|return|eq|equalizer|compressor|gate|limiter|'
               r'dynamics|expander|threshold|attack|release|decay|hold|'
               r'ratio|knee|makeup|overdrive|distortion|phaser|flanger|'
               r'chorus|reverb|delay|lfo|oscillator|envelope|adsr|filter|'
               r'cutoff|resonance|bandwidth|q.?factor|gain|pan|balance|'
               r'level|volume|fader|meter|loudness|true ?peak|rms|crest|'
               r'headroom|duck|side.?chain|bus|buses|channel|channels|'
               r'strip|mixer|mix ?console|effect|plug.?in|preset|plugin|'
               r'panner|aux|auxiliary|mono|stereo|surround)\b'),
    # ---- giao thuc / vong lap / chay ----
    ('transport', r'\b(locator|locators|marker|markers|cycle|transport|'
                  r'cursor|record|play|loop|shuttle|jog|scrub|rehearse|'
                  r'metronome|click|tempo|grid|snap|scroll|zoom|bar|bars|'
                  r'beat|beats|punch|pre.?roll|post.?roll|pre.?count|'
                  r'follow|sync|synchroni[sz]|timecode|drop ?frame|'
                  r'online|offline|auto.?scroll|jump|nudge|follow ?edit|'
                  r'cycle ?region|left |right )\b'),
    # ---- xuat / nhung / du an ----
    ('project', r'\b(export|import|render|bounce|pool|project|template|'
                r'preference|setup|profile|network|server|share|permission|'
                r'user|backup|auto ?save|save|archive|media ?bay|disk|'
                r'hard ?drive|media|file|format|directory|folder|path|'
                r'dialog|batch|queue|disk ?cache|thumbnail|wave ?file|'
                r'audio ?file|video ?file|omf|aaf|edl|xml|csv|AAF|OMF)\b'),
    # ---- MIDI Remote / dien tinh / giao dien ----
    ('ui', r'\b(window|toolbar|panel|menu|dialog|page|tab|context|shortcut|'
           r'key ?command|scroll ?bar|status ?line|info ?line|zone|'
           r'control ?room|inspector|arranger|ruler|zone|focus|visibility|'
           r'color ?set|colorize|show|hide|enable|disable|activate|'
           r'deactivate|toggle|open|close|collapse|expand|fold|unfold)\b'),

    # ---- nhan ngan: thu muc song song, bat CUOI cung ----
    # Do o tren, cac tu "Track" (149 lan), "Automation" (36), "Pitch" (37),
    # "Notehead" (37) xuat hien trong phan chua gan vung nao. Khong phai vi
    # chung khong thuoc linh vuc - ma vi regex cu khong co tu do. Vung nay
    # chi dung cho nhan quá ngan de quy ve mieng nao (Low, Apply, Sure, Link).
    ('nhan-le', r'^(low|high|medium|normal|global|local|standard|original|'
                r'combined|simple|advanced|manual|auto|off|on|none|any|'
                r'some|all|apply|link|unlink|reset|clear|sure|ok|cancel|'
                r'yes|no|done|more|less|min|max|total|estimated|approx|'
                r'view|views|apply|select|choose|add|remove|delete|erase|'
                r'edit|insert|create|duplicate|copy|move|rename|new|'
                r'between|before|after|above|below|greater|smaller)\b'
                r'[\w\s()%-]*$'),

    # ---- Track / khu vuc duong ----
    # 717 chuoi chua chu "track" - day la khu vuc lon nhat cua Cubase va
    # KHONG thuoc mixing, transport hay notation. Cung khong thuoc ui:
    # "Add Track...", "Active Track:", "Analyzer Track" deu la nhan cua chinh
    # Track, khong phai cua giao dien.
    ('track', r'\b(track|tracks|group ?track|audio ?track|instrument ?track|'
              r'midi ?track|fx ?track|folder ?track|vca ?track|video ?track|'
              r'voice ?track|arranger ?track|marker ?track|ruler ?track|'
              r'tracks? ?height|task ?bar|track ?list|show ?track|'
              r'active ?track|selected ?track|analy[sz]er|track ?version|'
              r'track ?control|track ?edit|track ?fader|track ?pan|'
              r'track ?mute|track ?solo|track ?record|track ?arm|'
              r'track ?lock|track ?freeze|track ?color|'
              r'track ?name|track ?volume|track ?panorama|track ?pitch)\b'),
]

COMPILED = [(n, re.compile(p, re.I)) for n, p in REGIONS]
V = re.compile(r'[\u00c0-\u024f\u1e00-\u1eff]')
VERB = re.compile(r'^(Add|Delete|Set|Get|Select|Choose|Enable|Disable|Show|Hide|'
                  r'Open|Close|Save|Load|Create|Remove|Insert|Apply|Reset|Copy|Move|'
                  r'Adjust|Change|Define|Activate|Deactivate|Toggle|Import|Export|'
                  r'Bounce|Render|Freeze|Quantize|Warp|Mute|Solo|Record|Play|'
                  r'Stop|Start|Next|Previous|Cancel|Confirm|Switch|Uncheck|Check|'
                  r'Mark|Unmark|Assign|Map|Link|Unlink|Sort|Filter|Search|'
                  r'Rename|Reload|Restore|Replace|Refresh|Reset)\b')

MAX_REGION = 3000


def region_of(k, en):
    """Vung cua mot chuoi, xep theo thu tu uu tien."""
    for name, rx in COMPILED:
        if rx.search(k) or rx.search(en):
            return name
    return None


def shape_of(en):
    e = en.strip()
    n = len(e)
    if n > 140:
        return 'van-xuoi'
    if e.endswith('?'):
        return 'cau-hoi'
    if VERB.match(e):
        return 'cau-lenh'
    if n <= 30:
        return 'nhan-ngan'
    if n <= 60:
        return 'ngan-31-60'
    return 'van-vua'


def main():
    args = sys.argv[1:]
    if '--region' in args:
        want = args[args.index('--region') + 1]
        n = 0
        for k, v in vi.items():
            if k in src and region_of(k, src[k]) == want:
                print(f'EN {src[k][:110]}')
                print(f'VI {v[:110]}')
                print()
                n += 1
                if n >= 40:
                    print(f'... con nhieu ({n} da in)')
                    break
        return

    by_region = collections.defaultdict(list)
    leftovers = []
    for k, v in vi.items():
        if k not in src:
            continue
        r = region_of(k, src[k])
        if r:
            by_region[r].append((k, v))
        else:
            leftovers.append((k, v))

    # ---- xuat 1 vung ra file de dich lan luot ----
    if '--dump' in sys.argv:
        out_dir = os.path.join(ROOT, 'keys', 'by_region')
        os.makedirs(out_dir, exist_ok=True)
        allkeys = dict(by_region)
        # phan con lai gom theo dang
        tail = collections.defaultdict(list)
        for k, v in leftovers:
            tail[shape_of(src[k])].append((k, v))
        allkeys.update(tail)

        total_written = 0
        for name, items in sorted(allkeys.items()):
            path = os.path.join(out_dir, name + '.txt')
            with open(path, 'w', encoding='utf-8', newline='\n') as f:
                for k, v in items:
                    f.write(f'EN\t{src[k]}\nVI\t{v}\n\n')
            total_written += len(items)
            kb = os.path.getsize(path) / 1024
            print(f'  {len(items):5}  {kb:6.0f} KB  {name}')
        print(f'\n{len(allkeys)} vung, {total_written} chuoi -> {out_dir}')
        print('Moi vung mot file, doc lien nhau de dich. Moi chuoi 2 dong: EN roi VI.')
        print('Khi sua: doi dong VI trong translations\\batches\\, khong sua file nay.')
        return

    # phan con lai theo DANG - de khong co nhom nao qua lon
    by_shape = collections.defaultdict(list)
    for k, v in leftovers:
        by_shape[shape_of(src[k])].append((k, v))

    total = len(vi)
    print(f'{total} chuoi — {len(by_region)} vung theo noi dung + '
          f'{len(by_shape)} nhom con lai theo dang\n')
    print(f'{"vung":14} {"so chuoi":>8} {"%":>5} {"TB VI":>6} {"chua dich":>9}')
    print('-' * 56)
    for name, items in sorted(by_region.items(), key=lambda x: -len(x[1])):
        avg = sum(len(v) for _k, v in items) / len(items)
        un = sum(1 for _k, v in items if not V.search(v))
        flag = '  <-- QUA LON' if len(items) > MAX_REGION else ''
        print(f'{name:14} {len(items):8} {100*len(items)/total:5.1f} '
              f'{avg:6.0f} {un:9}{flag}')
    print('-' * 56)
    rest = sum(len(x) for x in by_shape.values())
    for name, items in sorted(by_shape.items(), key=lambda x: -len(x[1])):
        avg = sum(len(v) for _k, v in items) / len(items)
        un = sum(1 for _k, v in items if not V.search(v))
        flag = '  <-- QUA LON' if len(items) > MAX_REGION else ''
        print(f'{name:14} {len(items):8} {100*len(items)/total:5.1f} '
              f'{avg:6.0f} {un:9}{flag}')
    print('-' * 56)
    print(f'{"TONG":14} {sum(len(x) for x in by_region.values()) + rest:8}')

    biggest = max(
        [(n, len(i)) for n, i in by_region.items()]
        + [(n, len(i)) for n, i in by_shape.items()])
    if biggest[1] > MAX_REGION:
        print(f'\n!! "{biggest[0]}" con {bigest[1]} chuoi — van qua lon de '
              f'dich mot luot.')
    else:
        print(f'\nVung lon nhat: {biggest[0]} ({biggest[1]} chuoi) — du de '
              f'xuat 1 vung/lan.')


if __name__ == '__main__':
    main()