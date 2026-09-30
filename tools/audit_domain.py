#!/usr/bin/env python3
"""Sau muc thuat ngu DAW cua AGENT.md §2, con nhieu cum tieng Anh chuyen nganh
chua bao gio duoc xet. Cong cu nay quet toan bo cac mien:

    ban nhac (score) · tron am (mixing) · MIDI · plug-in · video
    · media/warp · project setup · giao dien

Voi moi thuat ngu, hoi: ban dich CON GIU no, hay DA DICH? Neu da dich, cum
tieng Viet nao thay the - do la tu Viet dang bi dung sai.

Phan loai de khong duong: mot thuat ngu co the la DANH TU (phai giu) hoac
DONG TU (phai dich). `Insert Audio Part` la lenh -> 'Chen' dung. `Latency`
la nhan -> 'do tre' sai. Cac tu o dau chuoi, viet hoa chu dau, khong co tu
viet hoa thu hai = lenh (dong tu). Con lai coi nhu danh tu.

Khong ket luan. In ra de nguoi doc tu chot.
"""
import json, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = lambda *p: os.path.join(ROOT, *p)
V = re.compile(r'[\u00c0-\u024f\u1e00-\u1eff]')
WORD = re.compile(r'[A-Za-zÀ-ỹ\u0100-\u024f]+')

DOMAIN = {
    'BÀN NHẠC': """Clef Rest Stem Beam LedgerLine Accidental Notehead Tuplet
        Slur Tie Dot Dotting Rhythm Arpeggio Pedal Fingering Bowing Dynamics
        Coda Segno DalSegno Fine Fermata Breath Caesura Ottava ClefName
        GrandStaff Cue RepeatBar SegnoBar TempoMark TransposeInstrument
        InstrumentName PageBreak SystemBreak StaffGroup MeasureNumber""",

    'TRỘN ÂM': """Headroom Masking Crest Transient Envelope ADSR Attack Decay
        Sustain Release LFO Oscillator Sine Square Saw Random SampleHold
        RateSync Polarity PhaseInversion Feedback Bandwidth Notch Bell Shelf
        HighPass LowPass Cutoff Slope Q Resonance GainReduction Limiter
        Compressor Expander Gate GateSidechain Threshold Ratio Knee Makeup
        Lookahead DelayCompensation Compensation Dither Oversample Undo
        Bypass Inline Replace Append Normalize LoudnessRange TruePeak RMS
        MonoFoldDown Downmix Upmix Balance Panner Panning Lawfer Balance
        Trim GainStructure FaderGroup VCAGroup BusType SendEffect Return""",

    'MIDI': """NoteOn NoteOff ProgramChange PitchBend ChannelVoice PolyPressure
        Aftertouch Omni SysEx NRPN RPN MPE MTC PortMIDI DINJack ThruMerge
        Loopback Filter CCButton Controller Surface Mapping LearnAssign
        QuantizeStrength TimeCompress LiveInput SoftThru MergeType InOutSplit
        ListEditGraphic Colorize VelocityFixedLengthNoteResolution
        ConstrainDIATonicKeyScaleMode""",

    'PLUG-IN': """Driver LatencyCompensation DelayCompensation PluginClass
        VST2 VST3 AU AAX CLAP ShellPlugin VSTPort AudioPort EffectSlot
        PresetBank FactoryPreset UserPreset ProgramList VendorString
        PlugInformation ModulesGraph ChainSignal EQModule DynamicsModule
        CompareBypassCopy ReplacePlugin""",

    'VIDEO': """Timecode VITC LTC DropFrame NonDrop EDL AAF OMF RenderedFile
        VideoTrack VideoClip MovieObject ProxyPicture FreezeFrame Slip
        SyncPoint SyncTrial OfflineExport AlphaChannel Compositing
        VideoEvent MediaObject HandleLength""",

    'MEDIA / WARP': """WarpTab WarpMarker WarpFormant PreserveFormant
        TransientModel AudioWarp DetectionAlgorithm MultiBeatSample Slice
        ChopLoop WarpHandle Deconstruct ChopStart ChopLength TempoDetection
        RhythmicalSlice BeatChop MediaBayPool MediaBayAttribute""",

    'PROJECT': """TempoTrack TimeSignatureTrack MarkerTrack RulerTrack
        ArrangerTrack VideoTrackFX GroupChannel FXChannel FXReturn GroupBus
        VCAChannel InputBus OutputBus MainBus RecordingPath PoolPath
        AudioPath ProjectSetup DialogSetup ProgramOptions KeyCommand
        ImportAudioExportImagePool MediaLink RecordArming SoftRecord
        CycleRecord CycleFollow PunchInOut Autoscroll SyncScroll Zone
        ColorSet ProjectTemplates ProjectArchive Autosave BackupPath""",

    'GIAO DIỆN': """InspectorTab PanelChild ZoneLine ChannelZone RulerZone
        ArrangerZone StatusLine InfoLine ToolBox Toolbar ContextMenu
        ShortcutMenu FaderZone DropDown ComboBox EditLine ButtonLabel
        TabControl Splitter StatusBar ProgressBar ToolTip MenuEntry
        AcceleratorKey CommandKey DialogKey""",
}

# Giai doan lenh: chuoi bat dau bang thuat ngu viet hoa, khong tu viet hoa
# thu hai, va ngan -> dong tu. Nhung truong hop nay PHAI dich.
LEAD_VERB = set("""Insert Send Bypass Click Map Step Add Remove Delete Create
    Close Open Save Load Apply Reset Enable Disable Toggle Activate Deactivate
    Undo Redo Copy Cut Paste Duplicate Move Rename Import Export Bounce
    Render Freeze Quantize Warp Split Merge Trim Zoom Change Set Show Hide
    Scroll Select Unselect Snap Mute Solo Record Play Stop Start Jump Locate
    Navigate OpenUp Down Up Down Next Previous First Last All Any New
    Find Search Replace Print Refresh Reload Register Configure Connect
    Disconnect Deactivate Activate Solo Mute Arm Disarm Punch Cycle Repeat
    Capture Render Convert Adapt Match Detect Analyse Analyze Optimize
    Calculate Measure Count Sort Filter Group Ungroup Expand Collapse""".split())

vi = json.load(open(T('translations', 'vi.json'), encoding='utf-8'))
src = {}
for line in open(T('keys', 'all_strings.tsv'),
                 encoding='utf-8').read().splitlines()[1:]:
    if '\t' in line:
        k, u = line.split('\t', 1)
        src[k] = u


def is_imperative(en, term):
    """True neu 'term' dang o vi tri danh tu/loai tu -> phai dich."""
    if en.lower().startswith(term.lower() + ' '):
        rest = en[len(term):].strip()
        # 'Insert' + phan con lai viet hoa chu dau -> 'Insert Audio Part' la lenh
        if rest and rest[0].isupper() and not rest.startswith(tuple(
                w.capitalize() for w in () )):
            return True
        if not rest:
            return True
        # 'Delete Tool' - phan con lai chi 1 tu -> kha nang dong tu
        if len(re.findall(r"[A-Za-z][A-Za-z'-]*", rest)) <= 1:
            return True
    return False


def survey(term, domain):
    rx = re.compile(r'(?<![A-Za-z])' + re.escape(term).replace(r'\ ', r'\s+')
                    + r'(?![A-Za-z])', re.I)
    keep = 0
    added = collections.Counter()
    n_dich = 0
    samples = []
    for k, v in vi.items():
        if k not in src or not V.search(v):
            continue
        en = src[k]
        if not rx.search(en):
            continue
        if rx.search(v):
            keep += 1
            continue
        if is_imperative(en, term):
            continue
        n_dich += 1
        en_words = {w.lower() for w in WORD.findall(en)}
        for w in set(WORD.findall(v.lower())):
            if len(w) < 3 or w in en_words:
                continue
            if not re.search(r'[\u00c0-\u024f]', w):
                continue
            added[w] += 1
        if len(samples) < 2:
            samples.append((en, v))
    return keep, n_dich, added, samples


def main():
    only = [a for a in sys.argv[1:] if not a.startswith('-')]
    rows = []
    for domain, blob in DOMAIN.items():
        terms = [t for t in blob.split() if t]
        if only and domain not in only:
            continue
        for term in terms:
            if term in LEAD_VERB and not only:
                continue
            keep, n_dich, added, samples = survey(term, domain)
            if n_dich < 3:
                continue
            top = [(w, c) for w, c in added.most_common(3) if c >= 2]
            if not top:
                continue
            rows.append((n_dich, keep, domain, term, top, samples))

    if not rows:
        print('khong co ung vien')
        return
    print(f'{"dong":8} {"thuat ngu":16} {"giu":>4} {"dich":>5}  '
          f'dang dich thay bang')
    print('-' * 88)
    for n_dich, keep, domain, term, top, _ in sorted(rows, reverse=True):
        rep = ', '.join(f'{w} x{c}' for w, c in top)
        print(f'{domain:8} {term:16} {keep:4} {n_dich:5}  {rep}')
    print(f'\n{len(rows)} ung vien (>=3 chuoi bi dich, cum Viet >=2 lan)')

    if only:
        for n_dich, keep, domain, term, top, samples in rows:
            print(f'\n--- {term} ({domain}): giu {keep}, dich {n_dich}')
            for en, v in samples:
                print(f'    EN {en[:80]}')
                print(f'    VI {v[:80]}')


if __name__ == '__main__':
    main()