#!/usr/bin/env python3
"""Find capital Latin words in the middle of a Vietnamese value.

Rounds 31 to 34 found the largest single class in the short labels by reading:

    "Set Controller Type"   -> "Dat Loai Controller"
    "Set Crossfade Length"  -> "Dat Do dai Crossfade"
    "Set Color"             -> "Dat Mau"
    "Set Automation Value"  -> "Dat Gia tri Automation"

Vietnamese writes a noun lowercase mid-phrase, so "Dat Loai Controller" is
wrong three times over - and check_style cannot see it, because a capital
letter is a perfectly legal character.

The test: a value that HAS Vietnamese, where a capital Latin word appears
somewhere other than the first word, and that word is not a term the glossary
keeps in English. The kept-term list is deliberately small, so the output is a
lead list rather than a gate: it says where to look, and reading decides.

The list below is the set of words that are CORRECT in capitals mid-phrase,
either because the glossary keeps them in English or because they open a
proper name. Everything else that turns up is worth a look.

  python tools/find_stray_caps.py [minlen] [top]
"""
import json, re, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MIN = int(sys.argv[1]) if len(sys.argv) > 1 else 4
TOP = int(sys.argv[2]) if len(sys.argv) > 2 else 70

vi = json.load(open(os.path.join(ROOT, 'translations', 'vi.json'),
                    encoding='utf-8'))

# Words that legitimately carry a capital mid-phrase. Every entry is a term the
# glossary keeps in English, or a proper name, or the Vietnamese pronoun after a
# full stop inside the value.
KEEP = set("""
MIDI MIDIChannel MIDIRemote MIDIPorts MTC LTC MPE SMPTE OMF AAF ADM OLE XML
ASIO ASIOGuard WASAPI CoreAudio JACK AudioDevice JACKAudio FireWire WDM DirectSound
VST VST2 VST3 VSTi VSTPlugin VSTInstrument VSTPreset VSTModulator VSTEfx VSTMixer
AU AAX CLAP LV2 AudioUnit AudioComponent
MIXER MixConsole Mixdown VCA Sends Send EQ EQs Dynamics Compressor Limiter
Gate Gate2 Expander DeEsser Tube Compressor FET Multiband Dynamics Brickwall Liminer
Track Tracks Channel Channels Cue Cues Sends Bus Busses Instrument Instruments
Voice Voices Chord Chords Scale Scales Tension Tensions Voicing Voicings
Articulation Articulations Expression Expressions Note Notes Drum Drums
Foldback Talkback Metronome Grid Snap Quantize Warp WarpTab Tab Tabs
Project MediaBay Pool Sample Samples Snapshots Snapshot
Timecode Bars Beats Time Signature Key Signature Timebase Flexas
Automation Remote MIDI Remote Logic Link LinkGroup Unlink UnlinkGroup
Editor Editors Zone LowerZone MediaScore ScoreArranger
Nuendo SMPTE TEVE ProSampler HALion VSTConnect
Windows macOS Mac Linux iOS iPadOS
Cubase Nuendo Vienna ProRelay VEP VST Live Dexed
Web Editor Remote Control OnScreen
Synchro AudioTouch
Console Surround Center Front Left Right Side
LFE Atmos MPEG Auro Ambisonics
Folder Level Downmix SetUp Setup
Lanes LanesFilter
Crossfade Crossfades Hitpoint Hitpoints Slip Snap
WarpMarker WarpMarkers
Zoom Loop Cycle Punch PunchIn PunchOut
AbsDelay Delay Reverb Chorus Flanger Phaser Limiter Maximizer
EQCurve Spectrum Waveform Oscilloscope Vectorscope
Mute Solo SoloDefeat Listen Activate Deactivate
Shuffle FolderTrack MarkerTrack RulerArranger
Cropping CrossfadeTool FadesTool RangeTool SplitTool
MIDIFile MIDIMessage MIDIInsert MIDISend
Transport Location PunchPanel
Page PageSetup
Network Server Client WebDAV SFTP FTP
Preset Presets Program Programs User Users Permission Profile
MediaPool Sound Browser SoundSlot
MIDIInput MIDIOutput
Inserts Effects EQ Instruments Sends
DirectInput DirectOutput
MIXERBus GroupChannel
AudioInput AudioOutput
Camera Video Film
Apple Logitech Generic
NuendoConnect TimeDisplay
ResetThirds
Bounce Locate Import Export
Lanes AutomationParameter
AAX DAE
Prism TrueGrid
OS WindowsLinux
Patch Library
HLE
AoM
MultiChannel Mono
SetUp
MixConsole
Settings
Version
""".split())

# A VIETNAMESE LETTER, spelled with escapes on purpose. The obvious
# [A-ỿ] is U+0100 to U+1EF9, and it is WRONG: Vietnamese keeps its most
# common letters - a, a, e, e, o, o, u, u, d and their tone marks - in
# U+00C0 to U+00FF, which is BELOW the start of that range. So a value
# written entirely with those letters, like "Thêm bè", tested as NOT
# Vietnamese, and eight detectors built on this test were quietly looking
# at a subset of the map. Found in round 53, by a value that should have
# been reported and was not.
HAN = re.compile(r'[\u00c0-\u024f\u1e00-\u1eff]')
WORD = re.compile(r"[A-Za-z][A-Za-z0-9'/&\-]*")

rows = []
for k, v in vi.items():
    if len(v) < MIN or not HAN.search(v):
        continue
    # a value with more Vietnamese than the stray words is worth reading
    words = WORD.findall(v)
    han = len(HAN.findall(v))
    if han == 0:
        continue
    stray = []
    for i, w in enumerate(words):
        if i == 0:
            continue
        if not w[0].isupper():
            continue
        if w in KEEP:
            continue
        # after a sentence break a capital is fine
        pre = v[:v.index(w, 1)]
        if pre.rstrip().endswith(('.', ':', ';')):
            continue
        stray.append(w)
    if stray:
        rows.append((len(stray), k, v, stray))

rows.sort(key=lambda t: (-t[0], t[1]))
print(f'values with a capital Latin word mid-phrase: {len(rows)}')
print(f'showing {min(TOP, len(rows))}\n')
for n, k, v, stray in rows[:TOP]:
    print(f'  [{n}] {k[:62]!r}')
    print(f'      {v[:110]!r}')
    print(f'      stray: {stray}')
