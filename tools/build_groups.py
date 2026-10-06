#!/usr/bin/env python3
"""Build reverse-engineered fine-grained group classification for all 10,737 Cubase strings.

Scans:
  1. Skin & SRF templates (skin.srf, Sampler Track.srf, Drum Machine.srf... 797 templates)
  2. Fine-grained Cubase15.exe .rdata clusters (gap=300 bytes: 1,226 C++ function/module clusters)
  3. External Component DLL clusters (ScoringEngine, hubservice, admeditor, etc.)
  4. Official Key Commands categories (Key Commands.xml)
  5. Functional regions (keys/by_region verified functional domains)
  6. Precise syntactic tagging for standalone shortcuts and messages

Produces:
  - keys/groups.json: JSON mapping of key -> {domain, subgroup, source, confidence}
  - keys/grouped_strings.tsv: TSV table of all strings with groups and current Vietnamese text
"""
import os
import sys
import re
import html
import json
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from cubelib.pe import PE
from cubelib.srf import SRF

ORIGINAL_XML = os.path.join(ROOT, 'keys', 'translation_original.xml')
VI_JSON = os.path.join(ROOT, 'translations', 'vi.json')
OUT_JSON = os.path.join(ROOT, 'keys', 'groups.json')
OUT_TSV = os.path.join(ROOT, 'keys', 'grouped_strings.tsv')
GROUP_NAMES_JSON = os.path.join(ROOT, 'tools', 'group_names.json')


def get_variants(k):
    res = {k}
    u = html.unescape(k)
    res.add(u)
    for s in list(res):
        if '\\n' in s:
            res.add(s.replace('\\n', '\n'))
            res.add(s.replace('\\n', '\r\n'))
        if '\\t' in s:
            res.add(s.replace('\\t', '\t'))
        s_strip = s.strip()
        if len(s_strip) >= 3:
            res.add(s_strip)
    return res


def domain_of(subgroup, sample_key):
    s = subgroup.lower()
    k = sample_key.lower()

    # Exact semantic overrides for unambiguous core concepts
    if any(w in k for w in ('clef', 'stave', 'score editor', 'engraving')):
        return 'Score Editor & Notation'
    if any(w in k for w in ('metronome', 'count-in')):
        return 'Transport & Navigation'
    if any(w in k for w in ('chord track', 'chord pad', 'circle of fifths')):
        return 'Music Theory & Chords'
    if any(w in k for w in ('hitpoint', 'audiowarp')):
        return 'Audio & Processing'
    if any(w in k for w in ('mixconsole', 'side-chain')):
        return 'MixConsole & Routing'
    if any(w in k for w in ('quantize', 'note expression')):
        return 'MIDI & Sequencing'

    if any(w in s for w in ('score', 'notation', 'engrav', 'staff', 'stave', 'clef', 'pedal', 'dorico', 'scoringengine', 'chord symbols')) or any(w in k for w in ('clef', 'beam', 'tuplet', 'stave', 'ledger', 'stem')):
        return 'Score Editor & Notation'

    if any(w in s for w in ('transport', 'metronome', 'click', 'locator', 'marker', 'cycle', 'jog', 'scrub', 'tempo', 'bpm', 'timecode', 'preroll', 'postroll', 'count-in')):
        return 'Transport & Navigation'

    if any(w in s for w in ('mixconsole', 'mixer', 'fader', 'panner', 'pan ', 'equalizer', 'insert', 'send', 'side-chain', 'routing', 'bus', 'vca', 'channel', 'rack', 'automation', 'loudness', 'surround', 'downmix')):
        return 'MixConsole & Routing'

    if any(w in s for w in ('midi', 'quantize', 'controller', 'sysex', 'velocity', 'drum map', 'step input', 'pattern', 'expression map', 'swing')):
        return 'MIDI & Sequencing'

    if any(w in s for w in ('audio', 'warp', 'hitpoint', 'offline process', 'fade', 'crossfade', 'bounce', 'sampleeditor', 'audioplugs', 'alignment')):
        return 'Audio & Processing'

    if any(w in s for w in ('chord', 'voicing', 'scale', 'triad', 'cadence', 'circle of fifths', 'harmony', 'pads')):
        return 'Music Theory & Chords'

    if any(w in s for w in ('variaudio', 'pitch', 'formant')):
        return 'VariAudio & Pitch'

    if any(w in s for w in ('mediabay', 'soundbrowser', 'previewer', 'contentpack', 'vstsound', 'attribute', 'aspect')):
        return 'MediaBay & Sound Content'

    if any(w in s for w in ('export', 'mixdown', 'render', 'aaffilter', 'omffilter', 'admeditor', 'dawproject', 'video')):
        return 'Export & Delivery'

    if any(w in s for w in ('sampler track', 'drum machine', 'modulation fx', 'vstplugin', 'instrument', 'synth', 'plugin')):
        return 'Instruments & Plugins'

    if any(w in s for w in ('syncstation', 'hardware', 'midiport', 'studio', 'asio', 'vstconnect', 'eucon', '9-pin', 'serial port', 'machine control')):
        return 'Studio Setup & Hardware'

    if any(w in s for w in ('pref', 'command', 'workspace', 'colordialog', 'color setup', 'appearance', 'keycommands', 'keyboard')):
        return 'Preferences & Key Commands'

    if any(w in s for w in ('hubservice', 'file', 'save', 'open', 'backup', 'license', 'profile')):
        return 'System & Project File Operations'

    return 'Project & Timeline'


def build():
    print("Loading original translation keys...")
    src = open(ORIGINAL_XML, encoding='utf-8').read()
    all_keys = re.findall(r'<String Key="([^"]*)"', src)
    print(f"Total strings to classify: {len(all_keys):,}")

    variant_to_keys = {}
    for k in all_keys:
        for v in get_variants(k):
            variant_to_keys.setdefault(v, set()).add(k)

    # 1. SRF Templates (UI layout definitions)
    print("1. Scanning SRF skin templates...")
    srf_map = {}
    for sp in glob.glob(r'E:\Steinberg\Cubase 15\**\*.srf', recursive=True):
        try:
            srf = SRF.load(sp)
            xml = srf.skin_xml()
            if not xml:
                continue
            text = xml.decode('utf-8', 'replace')
            for m in re.finditer(r'<template\s+[^>]*name="([^"]+)"[^>]*>(.*?)</template>', text, re.S):
                tname = m.group(1)
                tbody = m.group(2)
                for attr in re.findall(r'\b(?:title|label|text|tooltip|caption|description)="([^"]+)"', tbody):
                    if attr in variant_to_keys:
                        for orig_k in variant_to_keys[attr]:
                            srf_map.setdefault(orig_k, tname)
        except Exception:
            pass
    print(f"   Strings matched to UI templates: {len(srf_map):,}")

    # 2. Key Commands (official categories for voting)
    print("2. Scanning Key Commands categories...")
    kc_path = os.path.expandvars(r'%APPDATA%\Steinberg\Cubase 15_64\Key Commands.xml')
    cat_of = {}
    kc_map = {}
    if os.path.exists(kc_path):
        kc_text = open(kc_path, encoding='utf-8').read()
        for cat, body in re.findall(r'<item>\s*<string name="Name" value="([^"]+)"\s*/>\s*<list name="Commands" type="list">(.*?)</list>', kc_text, re.S):
            for name in re.findall(r'<string name="Name" value="([^"]+)"\s*/>', body):
                for orig_k in variant_to_keys.get(name, [name]):
                    cat_of[orig_k] = cat
                    kc_map.setdefault(orig_k, cat)
    print(f"   Strings matched to Key Commands: {len(kc_map):,}")

    # 3. Functional regions for voting
    print("3. Scanning functional regions (keys/by_region)...")
    functional_files = {
        'audio.txt': 'Audio Processing',
        'midi.txt': 'MIDI & Sequencing',
        'mixing.txt': 'MixConsole & Routing',
        'transport.txt': 'Transport & Locators',
        'notation.txt': 'Score & Notation',
        'project.txt': 'Project & Arrangement',
        'track.txt': 'Track Controls',
        'ui.txt': 'User Interface'
    }
    functional_map = {}
    for fname, fdesc in functional_files.items():
        fpath = os.path.join(ROOT, 'keys', 'by_region', fname)
        if os.path.exists(fpath):
            for line in open(fpath, encoding='utf-8'):
                if line.startswith('EN\t'):
                    en_txt = line[3:].rstrip('\r\n')
                    for orig_k in variant_to_keys.get(en_txt, [en_txt]):
                        functional_map.setdefault(orig_k, fdesc)
    print(f"   Strings mapped in functional regions: {len(functional_map):,}")

    # 4. Cubase15.exe fine-grained .rdata clusters (gap = 300 bytes)
    print("4. Scanning Cubase15.exe C++ .rdata clusters (gap=300)...")
    pe = PE(r'E:\Steinberg\Cubase 15\Cubase15.exe')
    rdata_sec = [s for s in pe.sections if s.name == '.rdata'][0]
    image = bytes(pe.bin.data)
    rdata = image[rdata_sec.raw_ptr:rdata_sec.raw_ptr + rdata_sec.raw_size]
    rdata_base = rdata_sec.raw_ptr

    ASCII_RX = re.compile(rb'[\x20-\x7e]{3,}')
    U16_RX = re.compile(rb'(?:[\x20-\x7e]\x00){3,}')

    rdata_offsets = {}
    for rx, enc in ((ASCII_RX, 'latin-1'), (U16_RX, 'utf-16-le')):
        for m in rx.finditer(rdata):
            txt = m.group().decode(enc, 'replace')
            if txt in variant_to_keys:
                off = rdata_base + m.start()
                for k in variant_to_keys[txt]:
                    if k not in rdata_offsets:
                        rdata_offsets[k] = off

    manual_names = {}
    if os.path.exists(GROUP_NAMES_JSON):
        manual_names = {int(k, 16): v for k, v in json.load(open(GROUP_NAMES_JSON, encoding='utf-8')).items()}

    sorted_offsets = sorted(rdata_offsets.items(), key=lambda kv: kv[1])
    clusters = []
    GAP = 300
    for k, off in sorted_offsets:
        if clusters and off - clusters[-1][-1][1] <= GAP:
            clusters[-1].append((k, off))
        else:
            clusters.append([(k, off)])

    exe_cluster_map = {}
    for idx, c in enumerate(clusters):
        start = min(o for _, o in c)
        name = None
        for m_off, m_name in manual_names.items():
            if abs(start - m_off) <= 2000:
                name = m_name
                break
        if not name:
            votes = {}
            for k, _ in c:
                if k in cat_of:
                    votes[cat_of[k]] = votes.get(cat_of[k], 0) + 1
            if votes:
                top_cat = max(votes.items(), key=lambda kv: kv[1])[0]
                name = f"{top_cat} (C++ 0x{start:06X})"
        if not name:
            fvotes = {}
            for k, _ in c:
                if k in functional_map:
                    fvotes[functional_map[k]] = fvotes.get(functional_map[k], 0) + 1
            if fvotes:
                top_f = max(fvotes.items(), key=lambda kv: kv[1])[0]
                name = f"{top_f} (C++ 0x{start:06X})"
        if not name:
            name = f"Core UI Module @ 0x{start:08X}"

        for k, off in c:
            exe_cluster_map[k] = name

    print(f"   Strings placed in EXE .rdata clusters: {len(exe_cluster_map):,}")

    # 5. DLL Component Clusters
    print("5. Scanning Component DLLs...")
    special_dlls = ['ScoringEngine.dll', 'admeditor.dll', 'hubservice.dll', 'DAWproject.dll',
                    'OMFFilter.dll', 'aaffilter.dll', 'audioalignment.dll', 'audio2chords.dll',
                    'vstconnect.dll', 'videoengine.dll', 'Sampler Track.dll', 'Drum Machine.dll']
    ASCII_CSTR = re.compile(rb'[\x09\x0a\x0d\x20-\x7e]{3,}\x00')
    U16_CSTR = re.compile(rb'(?:[\x09\x0a\x0d\x20-\x7e]\x00){3,}\x00\x00')

    dll_map = {}
    for sdll in special_dlls:
        matched_paths = glob.glob(os.path.join(r'E:\Steinberg\Cubase 15', '**', sdll), recursive=True)
        for dp in matched_paths:
            dname = os.path.splitext(os.path.basename(dp))[0]
            data = open(dp, 'rb').read()
            for rx, dec in ((ASCII_CSTR, 'latin-1'), (U16_CSTR, 'utf-16-le')):
                for m in rx.finditer(data):
                    try:
                        txt = m.group()[:-1 if dec == 'latin-1' else -2].decode(dec)
                    except Exception:
                        continue
                    if txt in variant_to_keys:
                        for orig_k in variant_to_keys[txt]:
                            dll_map.setdefault(orig_k, f"Component: {dname}")

    print(f"   Strings found in Component DLLs: {len(dll_map):,}")

    # 6. Classify every string
    print("Classifying into fine-grained subgroups and domains...")
    result = {}
    subgroup_domains = {}

    for k in all_keys:
        if k in srf_map:
            sub = f"Template: {srf_map[k]}"
            src_tag = f"SRF:{srf_map[k]}"
            conf = "high"
        elif k in kc_map:
            sub = f"Command: {kc_map[k]}"
            src_tag = f"KC:{kc_map[k]}"
            conf = "high"
        elif k in dll_map:
            sub = f"DLL: {dll_map[k]}"
            src_tag = f"DLL:{dll_map[k]}"
            conf = "high"
        elif k in exe_cluster_map:
            sub = f"Cluster: {exe_cluster_map[k]}"
            src_tag = f"EXE:{exe_cluster_map[k]}"
            conf = "high"
        elif k in functional_map:
            sub = f"Feature: {functional_map[k]}"
            src_tag = f"REGION:{functional_map[k]}"
            conf = "high"
        else:
            kl = k.lower()
            if '[key]' in kl or re.search(r'\b(alt|ctrl|shift|del|enter|esc|home|end|pad)\b', kl):
                sub = "Keyboard Shortcuts & Modifiers"
                src_tag = "SYNTAX:shortcut"
            elif 'marker' in kl or 'locator' in kl:
                sub = "Locators & Position Jump"
                src_tag = "SYNTAX:locator"
            elif 'downmix' in kl:
                sub = "MixConsole Downmix Presets"
                src_tag = "SYNTAX:downmix"
            elif 'auto save' in kl or 'corrupt' in kl:
                sub = "Project Auto-Save & Recovery"
                src_tag = "SYNTAX:recovery"
            elif 'ambisonic' in kl:
                sub = "Ambisonics & Spatial Audio"
                src_tag = "SYNTAX:ambisonics"
            elif 'loudness' in kl or 'bwf' in kl:
                sub = "Loudness & Broadcast Audio"
                src_tag = "SYNTAX:loudness"
            else:
                sub = "General Interface Labels"
                src_tag = "SYNTAX:general"
            conf = "medium"

        if sub not in subgroup_domains:
            subgroup_domains[sub] = domain_of(sub, k)
        dom = subgroup_domains[sub]

        result[k] = {
            'domain': dom,
            'subgroup': sub,
            'source': src_tag,
            'confidence': conf
        }

    # Load Vietnamese map
    vi_map = {}
    if os.path.exists(VI_JSON):
        vi_map = json.load(open(VI_JSON, encoding='utf-8'))

    # Save JSON
    with open(OUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"Saved: {OUT_JSON} ({os.path.getsize(OUT_JSON):,} bytes)")

    # Save TSV
    rows = [["key", "domain", "subgroup", "source", "confidence", "vietnamese"]]
    for k in all_keys:
        info = result[k]
        vi_text = vi_map.get(k, "")
        rows.append([k, info['domain'], info['subgroup'], info['source'], info['confidence'], vi_text])

    with open(OUT_TSV, 'w', encoding='utf-8') as f:
        for r in rows:
            clean_r = [field.replace('\t', ' ').replace('\r', '').replace('\n', '\\n') for field in r]
            f.write('\t'.join(clean_r) + '\n')
    print(f"Saved: {OUT_TSV} ({os.path.getsize(OUT_TSV):,} bytes)")

    distinct_subs = set(v['subgroup'] for v in result.values())
    distinct_doms = set(v['domain'] for v in result.values())
    print(f"\nCOMPLETED: 10,737 strings classified into {len(distinct_doms)} Domains and {len(distinct_subs):,} fine-grained Subgroups!")


def main():
    build()


if __name__ == '__main__':
    main()
