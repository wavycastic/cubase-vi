#!/usr/bin/env python3
"""Công cụ duyệt và quản lý 2.552 nhóm con (subgroups) của Cubase từ RE.

Cách dùng:
    python tools/group.py                               # Tóm tắt 14 domain chính & số nhóm con
    python tools/group.py -d Audio --subgroups          # Liệt kê mọi nhóm con của domain Audio
    python tools/group.py -g "Metronome"                # Xem các chuỗi trong nhóm con Metronome
    python tools/group.py -g "Hitpoints"                # Xem các chuỗi trong nhóm con Hitpoints
    python tools/group.py -k "Spike"                    # Tra cứu ngữ cảnh & nhóm con của một chuỗi
    python tools/group.py -d Transport -n 20 -p 1       # Xem trang 1 (20 chuỗi) của Transport
    python tools/group.py --export-subgroup "Hitpoints" out.json  # Xuất 1 nhóm con ra JSON để dịch
    python tools/group.py --rebuild                     # Quét RE lại toàn bộ Cubase
"""
import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GROUPS_JSON = os.path.join(ROOT, 'keys', 'groups.json')
VI_JSON = os.path.join(ROOT, 'translations', 'vi.json')


def load_data():
    if not os.path.exists(GROUPS_JSON):
        print("Chưa có keys/groups.json, đang chạy quét RE...")
        import build_groups
        build_groups.main()

    with open(GROUPS_JSON, encoding='utf-8') as f:
        groups = json.load(f)

    vi = {}
    if os.path.exists(VI_JSON):
        with open(VI_JSON, encoding='utf-8') as f:
            vi = json.load(f)

    return groups, vi


def print_summary(groups):
    total = len(groups)
    domains = {}
    subgroups = {}

    for k, info in groups.items():
        d = info['domain']
        s = info['subgroup']
        domains[d] = domains.get(d, 0) + 1
        subgroups.setdefault(d, set()).add(s)

    total_sub = sum(len(s) for s in subgroups.values())

    print("=" * 80)
    print(f" TỔNG HỢP RE CUBASE: {total:,} CHUỖI -> {len(domains)} DOMAIN & {total_sub:,} NHÓM CON (SUBGROUPS)")
    print("=" * 80)
    print(f" {'STT':<4} {'Domain (Nhóm chức năng)':<35} {'Số chuỗi':>10} {'Tỉ lệ':>8} {'Số nhóm con':>14}")
    print("-" * 80)

    idx = 1
    for d, count in sorted(domains.items(), key=lambda kv: kv[1], reverse=True):
        pct = count * 100.0 / total
        num_sub = len(subgroups.get(d, set()))
        print(f" {idx:<4} {d:<35} {count:>10,} {pct:>7.1f}% {num_sub:>14,}")
        idx += 1

    print("=" * 80)
    print("Ví dụ tra cứu:")
    print("  python tools/group.py -d Audio --subgroups    # Liệt kê tất cả nhóm con của Audio")
    print("  python tools/group.py -g \"Hitpoints\"          # Đọc riêng nhóm con Hitpoints để dịch")
    print("  python tools/group.py -k \"Spike\"              # Tra cứu một chuỗi cụ thể thuộc nhóm nào")


def list_subgroups(groups, dom_query=None):
    domains = {}
    for k, info in groups.items():
        d = info['domain']
        s = info['subgroup']
        domains.setdefault(d, {}).setdefault(s, []).append(k)

    q = dom_query.lower() if dom_query else ""
    matched_domains = [d for d in domains if q in d.lower()]

    if not matched_domains:
        print(f"Không tìm thấy domain nào khớp với '{dom_query}'.")
        return

    for d in matched_domains:
        subs = domains[d]
        total_d = sum(len(v) for v in subs.values())
        print("=" * 80)
        print(f" [{d}] — {total_d:,} chuỗi chia thành {len(subs):,} nhóm con:")
        print("=" * 80)
        for s, klist in sorted(subs.items(), key=lambda kv: len(kv[1]), reverse=True):
            sample = klist[0] if len(klist) == 1 else f"{klist[0]!r}, {klist[1]!r}..."
            print(f"  • {s:<55} ({len(klist):>3} chuỗi) -> e.g. {sample}")


def show_subgroup(groups, vi, sub_query, limit=100):
    q = sub_query.lower()
    matched = []
    for k, info in groups.items():
        if q in info['subgroup'].lower():
            matched.append((k, info))

    if not matched:
        print(f"Không tìm thấy nhóm con nào khớp với '{sub_query}'.")
        return

    print("=" * 80)
    print(f" KẾT QUẢ CHO NHÓM CON KHỚP VỚI: '{sub_query}' (Tổng: {len(matched):,} chuỗi)")
    print("=" * 80)

    for i, (k, info) in enumerate(matched[:limit]):
        v = vi.get(k, "[Chưa dịch]")
        print(f"{i + 1:>3}. [{info['domain']} > {info['subgroup']}]")
        print(f"     EN: {k}")
        print(f"     VI: {v}")
        print(f"     RE: {info['source']} ({info['confidence']})")
        print()

    if len(matched) > limit:
        print(f"... Còn {len(matched) - limit} chuỗi khác trong nhóm này.")


def show_domain(groups, vi, dom_query, limit=30, page=1):
    q = dom_query.lower()
    matched = []
    for k, info in groups.items():
        if q in info['domain'].lower():
            matched.append((k, info))

    if not matched:
        print(f"Không tìm thấy domain nào khớp với '{dom_query}'.")
        return

    matched.sort(key=lambda item: (item[1]['subgroup'], item[0]))
    total = len(matched)
    start = (page - 1) * limit
    end = min(start + limit, total)
    total_pages = (total + limit - 1) // limit

    print("=" * 80)
    print(f" DOMAIN: {matched[0][1]['domain']} (Tổng: {total:,} chuỗi | Trang {page}/{total_pages})")
    print("=" * 80)

    for i in range(start, end):
        k, info = matched[i]
        v = vi.get(k, "[Chưa dịch]")
        print(f"{i + 1:>4}. [{info['subgroup']}]")
        print(f"      EN: {k}")
        print(f"      VI: {v}")
        print(f"      RE: {info['source']}")
        print()

    if end < total:
        print(f"... Còn {total - end} chuỗi. Xem trang kế: -d \"{dom_query}\" -p {page + 1} -n {limit}")


def lookup_key(groups, vi, query):
    q = query.lower()
    hits = []
    for k, info in groups.items():
        if q in k.lower():
            hits.append((k, info))

    if not hits:
        print(f"Không tìm thấy chuỗi nào chứa '{query}'.")
        return

    print(f"Tìm thấy {len(hits)} chuỗi khớp với '{query}':\n")
    for i, (k, info) in enumerate(hits[:30]):
        v = vi.get(k, "[Chưa dịch]")
        print(f"{i + 1:>3}. EN: {k}")
        print(f"     VI: {v}")
        print(f"     Domain:    {info['domain']}")
        print(f"     Subgroup:  {info['subgroup']}")
        print(f"     Nguồn RE:  {info['source']} ({info['confidence']})")
        print("-" * 65)

    if len(hits) > 30:
        print(f"... và {len(hits) - 30} chuỗi khác.")


def export_subgroup(groups, vi, sub_query, out_path):
    q = sub_query.lower()
    out = {}
    for k, info in groups.items():
        if q in info['subgroup'].lower():
            out[k] = vi.get(k, "")

    if not out:
        print(f"Không tìm thấy chuỗi nào trong nhóm con khớp với '{sub_query}'.")
        return

    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print(f"Đã xuất {len(out):,} chuỗi của nhóm con '{sub_query}' vào file: {out_path}")


def export_domain(groups, vi, dom_query, out_path):
    q = dom_query.lower()
    out = {}
    for k, info in groups.items():
        if q in info['domain'].lower():
            out[k] = {
                'subgroup': info['subgroup'],
                'source': info['source'],
                'en': k,
                'vi': vi.get(k, "")
            }

    if not out:
        print(f"Không tìm thấy chuỗi nào trong domain khớp với '{dom_query}'.")
        return

    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print(f"Đã xuất {len(out):,} chuỗi của domain '{dom_query}' vào file: {out_path}")


def export_all_domains(groups, vi, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    domain_slugs = {
        'Project & Timeline': '01_project_timeline.json',
        'MixConsole & Routing': '02_mixconsole_routing.json',
        'Score Editor & Notation': '03_score_notation.json',
        'MIDI & Sequencing': '04_midi_sequencing.json',
        'Transport & Navigation': '05_transport_navigation.json',
        'Audio & Processing': '06_audio_processing.json',
        'Music Theory & Chords': '07_music_theory_chords.json',
        'Preferences & Key Commands': '08_preferences_commands.json',
        'Export & Delivery': '09_export_delivery.json',
        'System & Project File Operations': '10_system_file_ops.json',
        'Studio Setup & Hardware': '11_studio_hardware.json',
        'MediaBay & Sound Content': '12_mediabay_content.json',
        'Instruments & Plugins': '13_instruments_plugins.json',
        'VariAudio & Pitch': '14_variaudio_pitch.json'
    }

    buckets = {d: {} for d in domain_slugs}
    for k, info in groups.items():
        d = info['domain']
        if d in buckets:
            buckets[d][k] = {
                'subgroup': info['subgroup'],
                'source': info['source'],
                'en': k,
                'vi': vi.get(k, "")
            }

    for d, fname in domain_slugs.items():
        p = os.path.join(out_dir, fname)
        with open(p, 'w', encoding='utf-8') as f:
            json.dump(buckets[d], f, ensure_ascii=False, indent=2)
        print(f"  Đã xuất {len(buckets[d]):>5} chuỗi -> {fname}")

    print(f"\nĐã xuất toàn bộ 10,737 chuỗi vào thư mục: {out_dir}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-d', '--domain', help='Lọc chuỗi theo domain (Audio, Transport, MixConsole...)')
    parser.add_argument('-g', '--subgroup', help='Lọc chuỗi theo subgroup cụ thể (Hitpoints, Quantize, Metronome...)')
    parser.add_argument('-s', '--subgroups', action='store_true', help='Liệt kê danh sách tất cả nhóm con của domain')
    parser.add_argument('-k', '--key', help='Tra cứu ngữ cảnh & nhóm con của một chuỗi cụ thể')
    parser.add_argument('-n', '--limit', type=int, default=30, help='Số chuỗi hiển thị mỗi lần (mặc định 30)')
    parser.add_argument('-p', '--page', type=int, default=1, help='Số trang cần xem (mặc định 1)')
    parser.add_argument('--export-subgroup', nargs=2, metavar=('SUBGROUP', 'OUT_FILE'), help='Xuất riêng 1 nhóm con ra JSON để dịch')
    parser.add_argument('--export-domain', nargs=2, metavar=('DOMAIN', 'OUT_FILE'), help='Xuất toàn bộ 1 domain ra JSON')
    parser.add_argument('--export-all-domains', nargs='?', const='translations/by_domain', metavar='DIR', help='Xuất toàn bộ 14 domain thành 14 file JSON riêng biệt')
    parser.add_argument('--rebuild', action='store_true', help='Quét RE lại toàn bộ binary và tạo lại bảng phân nhóm')

    args = parser.parse_args()

    if args.rebuild:
        import build_groups
        build_groups.main()
        return 0

    groups, vi = load_data()

    if args.export_all_domains:
        export_all_domains(groups, vi, args.export_all_domains)
    elif args.export_domain:
        export_domain(groups, vi, args.export_domain[0], args.export_domain[1])
    elif args.export_subgroup:
        export_subgroup(groups, vi, args.export_subgroup[0], args.export_subgroup[1])
    elif args.subgroups:
        list_subgroups(groups, args.domain)
    elif args.key:
        lookup_key(groups, vi, args.key)
    elif args.subgroup:
        show_subgroup(groups, vi, args.subgroup, args.limit)
    elif args.domain:
        show_domain(groups, vi, args.domain, args.limit, args.page)
    else:
        print_summary(groups)

    return 0


if __name__ == '__main__':
    sys.exit(main())
