#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from collections import defaultdict

def pv(s):
    if not s: return 0
    s = str(s).strip().replace(' ', '')
    if s in ['-', '', '0']: return 0
    s = s.replace('.', '').replace(',', '')
    try: return float(s)
    except: return 0

def tax109(tnct):
    if tnct <= 0: return 0
    t, r = 0, tnct
    for cap, rate in [(10e6,.05),(20e6,.10),(30e6,.20),(60e6,.30),(1e15,.35)]:
        t += min(r, cap) * rate
        r -= cap
        if r <= 0: break
    return t

def npt_from_old(gt):
    return max(0, round((gt - 11_000_000) / 4_400_000))

def gt109(npt):
    return 15_500_000 + npt * 6_200_000

# ---- READ SHEET 1 ----
r1 = []
with open(r'D:\Học Claude code\Skill\output\temp_sheet1.csv', encoding='utf-8-sig') as f:
    lines = f.readlines()
for i, ln in enumerate(lines):
    if i < 2: continue
    p = ln.strip().split(',')
    if len(p) < 4 or not p[1].strip(): continue
    thu_nhap = pv(p[2])
    if thu_nhap <= 0: continue
    gt_str = p[9].strip() if len(p) > 9 else '0'
    r1.append({
        'thang': p[0].strip(), 'ten': p[1].strip(),
        'thu_nhap': thu_nhap, 'thue_khau': pv(p[3]),
        'loai': p[4].strip() if len(p) > 4 else '',
        'bhxh': pv(p[7]) if len(p) > 7 else 0,
        'cd': pv(p[8]) if len(p) > 8 else 0,
        'gt_old': pv(gt_str) if gt_str != '-' else 0,
        'has_bhxh': pv(p[6]) > 0 if len(p) > 6 else False
    })

# ---- READ SHEET 2 ----
r2 = []
with open(r'D:\Học Claude code\Skill\output\temp_sheet2.csv', encoding='utf-8-sig') as f:
    lines = f.readlines()
for i, ln in enumerate(lines):
    if i < 2: continue
    p = ln.strip().split(',')
    if len(p) < 5 or not p[1].strip(): continue
    thu_nhap = pv(p[3])
    if thu_nhap <= 0: continue
    r2.append({
        'thang': p[0].strip(), 'ten': p[1].strip(),
        'thu_nhap': thu_nhap, 'thue_khau': pv(p[4])
    })

# ---- BASIC STATS ----
months1 = sorted(set(r['thang'] for r in r1))
months2_raw = sorted(set(r['thang'] for r in r2))
names1 = set(r['ten'] for r in r1)
names2 = set(r['ten'] for r in r2)
all_names = names1 | names2
bhxh_names = set(r['ten'] for r in r1 if r['has_bhxh'])
s2_only = names2 - names1

print("=" * 60)
print("A. TỔNG QUAN NHÂN SỰ")
print("=" * 60)
print(f"Tổng số nhân viên (unique toàn bộ): {len(all_names)}")
print(f"  - Sheet 1 (có BHXH/Lương hiệu quả): {len(names1)} tên")
print(f"  - Sheet 2 (Phụ lục 02 / 10% flat): {len(names2)} tên")
print(f"  - Người xuất hiện trong cả 2 sheet: {len(names1 & names2)}")
print(f"  - Người chỉ có ở Sheet 2: {len(s2_only)}")
print(f"Người có BHXH (Phụ lục 01): {len(bhxh_names)}")
print(f"Kỳ dữ liệu Sheet 1: {', '.join(months1)}")
print(f"Kỳ dữ liệu Sheet 2: {', '.join(months2_raw[:15])}{'...' if len(months2_raw) > 15 else ''}")
print(f"Tổng kỳ trong Sheet 2: {len(months2_raw)} kỳ")

# ---- FINANCIAL TOTALS ----
s1_income = sum(r['thu_nhap'] for r in r1)
s1_bhxh = sum(r['bhxh'] for r in r1)
s1_tax = sum(r['thue_khau'] for r in r1)
s2_income = sum(r['thu_nhap'] for r in r2)
s2_tax = sum(r['thue_khau'] for r in r2)

# ---- PER-PERSON TAX RECALC ----
person = defaultdict(lambda: {'income': 0, 'tax_src': 0, 'tax_109': 0, 'bhxh': 0})

# Lương cứng: recalculate with Luật 109
for r in r1:
    if r['loai'] != 'Lương cứng': continue
    n = r['ten']
    person[n]['income'] += r['thu_nhap']
    person[n]['tax_src'] += r['thue_khau']
    person[n]['bhxh'] += r['bhxh']
    npt = npt_from_old(r['gt_old'])
    tnct = max(0, r['thu_nhap'] - r['bhxh'] - r['cd'] - gt109(npt))
    person[n]['tax_109'] += tax109(tnct)

# Lương hiệu quả: keep 10%
for r in r1:
    if r['loai'] != 'Lương hiệu quả': continue
    n = r['ten']
    person[n]['income'] += r['thu_nhap']
    person[n]['tax_src'] += r['thue_khau']
    person[n]['tax_109'] += r['thue_khau']

# Sheet 2: keep 10%
for r in r2:
    n = r['ten']
    person[n]['income'] += r['thu_nhap']
    person[n]['tax_src'] += r['thue_khau']
    person[n]['tax_109'] += r['thue_khau']

total_tax_109 = sum(v['tax_109'] for v in person.values())
total_tax_src = sum(v['tax_src'] for v in person.values())
total_income = sum(v['income'] for v in person.values())
total_bhxh = sum(v['bhxh'] for v in person.values())

print()
print("=" * 60)
print("B. CHỈ SỐ TÀI CHÍNH")
print("=" * 60)
print(f"Tổng thu nhập đã chi trả (cả 2 sheet):  {total_income:>20,.0f} VND")
print(f"  - Sheet 1 (Lương cứng + Hiệu quả):    {s1_income:>20,.0f} VND")
print(f"  - Sheet 2 (Phụ lục 02):                {s2_income:>20,.0f} VND")
print(f"Tổng BHXH đã khấu trừ (Sheet 1):        {total_bhxh:>20,.0f} VND")
print(f"Tổng thuế TNCN đã khấu trừ tại nguồn:   {total_tax_src:>20,.0f} VND")
print(f"  - Sheet 1:                             {s1_tax:>20,.0f} VND")
print(f"  - Sheet 2:                             {s2_tax:>20,.0f} VND")
print(f"Tổng thuế TNCN phải nộp (Luật 109):     {total_tax_109:>20,.0f} VND")
diff = total_tax_109 - total_tax_src
if diff > 0:
    print(f"Chênh lệch (CÒN PHẢI NỘP THÊM):         {diff:>20,.0f} VND")
else:
    print(f"Chênh lệch (ĐƯỢC HOÀN):                  {abs(diff):>20,.0f} VND")

# ---- BRACKET DISTRIBUTION ----
by_name_lc = defaultdict(list)
for r in r1:
    if r['loai'] == 'Lương cứng':
        by_name_lc[r['ten']].append(r)

brackets = {'no': [], 'b1': [], 'b2': [], 'b3': [], 'b45': []}
for name, recs in by_name_lc.items():
    n = len(recs)
    npt = max(npt_from_old(r['gt_old']) for r in recs)
    avg_inc = sum(r['thu_nhap'] for r in recs) / n
    avg_bhxh = sum(r['bhxh'] for r in recs) / n
    avg_cd = sum(r['cd'] for r in recs) / n
    avg_tnct = max(0, avg_inc - avg_bhxh - avg_cd - gt109(npt))

    if avg_tnct <= 0: brackets['no'].append(name)
    elif avg_tnct <= 10e6: brackets['b1'].append(name)
    elif avg_tnct <= 30e6: brackets['b2'].append(name)
    elif avg_tnct <= 60e6: brackets['b3'].append(name)
    else: brackets['b45'].append(name)

print()
print("=" * 60)
print("C. PHÂN BỔ THEO BẬC THUẾ (Luật 109 - dựa trên Lương cứng)")
print("=" * 60)
total_lc = sum(len(v) for v in brackets.values())
print(f"Không phải nộp (TNCT ≤ 0):              {len(brackets['no']):>3} người")
print(f"Bậc 1  (TNCT ≤ 10tr/tháng, 5%):         {len(brackets['b1']):>3} người")
print(f"Bậc 2  (TNCT 10-30tr/tháng, 10%):       {len(brackets['b2']):>3} người")
print(f"Bậc 3  (TNCT 30-60tr/tháng, 20%):       {len(brackets['b3']):>3} người")
print(f"Bậc 4-5 (TNCT > 60tr/tháng, 30-35%):   {len(brackets['b45']):>3} người")
print(f"[Tổng người trong bảng lương cứng: {total_lc}]")

# ---- TOP & BOTTOM ----
print()
print("=" * 60)
print("D. TOP & BOTTOM")
print("=" * 60)
by_tax = sorted(person.items(), key=lambda x: x[1]['tax_109'], reverse=True)
by_income = sorted(person.items(), key=lambda x: x[1]['income'])

print("Top 3 đóng thuế nhiều nhất (Luật 109):")
for name, v in by_tax[:3]:
    print(f"  {name:<35} Thuế: {v['tax_109']:>12,.0f}  |  Thu nhập: {v['income']:>15,.0f}")

print("\n3 người thu nhập thấp nhất:")
for name, v in by_income[:3]:
    print(f"  {name:<35} Thu nhập: {v['income']:>12,.0f}")

# ---- ANOMALIES ----
print()
print("=" * 60)
print("E. CẢNH BÁO BẤT THƯỜNG (chênh lệch thuế > 1 triệu VND)")
print("=" * 60)
anomalies = []
for n, v in person.items():
    diff = v['tax_109'] - v['tax_src']
    if abs(diff) > 1_000_000:
        anomalies.append((n, v['tax_src'], v['tax_109'], diff))

anomalies.sort(key=lambda x: abs(x[3]), reverse=True)
if anomalies:
    print(f"{'Tên':<35} {'Đã khấu trừ':>14} {'Luật 109':>14} {'Chênh lệch':>14}")
    print("-" * 80)
    for name, src, l109, d in anomalies[:15]:
        marker = "(+thêm)" if d > 0 else "(hoàn)"
        print(f"  {name:<33} {src:>14,.0f} {l109:>14,.0f} {d:>+14,.0f} {marker}")
    if len(anomalies) > 15:
        print(f"  ... và {len(anomalies) - 15} người khác")
else:
    print("  Không có bất thường đáng kể.")

print()
print("=" * 60)
print("Gợi ý: /tncn-generator (từ CSV) hoặc /tncn-sheets-sync (từ Google Sheets)")
print("       để tạo bộ hồ sơ quyết toán 05/QTT-TNCN đầy đủ.")
print("=" * 60)
