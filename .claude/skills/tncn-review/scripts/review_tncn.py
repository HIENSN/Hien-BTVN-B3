"""
Skill 3 - tncn-review
Phan tich nhanh bang luong, xuat file tong quan thue TNCN.
"""
import sys, io
from collections import defaultdict
from datetime import datetime
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

try:
    import openpyxl
except ImportError:
    print("ERROR: pip install openpyxl"); sys.exit(1)

GIAM_TRU_BAN_THAN = 15_500_000
OUTPUT_DIR = Path("output")

def parse_vnd(v):
    if v is None: return 0
    if isinstance(v, (int, float)): return int(round(v))
    try: return int(str(v).strip().replace(".","").replace(",","").replace(" ","") or 0)
    except: return 0

def calc_thue(tnct):
    if tnct <= 0: return 0
    t = min(tnct, 10_000_000) * 0.05
    if tnct > 10_000_000:  t += (min(tnct, 30_000_000)  - 10_000_000)  * 0.10
    if tnct > 30_000_000:  t += (min(tnct, 60_000_000)  - 30_000_000)  * 0.20
    if tnct > 60_000_000:  t += (min(tnct, 100_000_000) - 60_000_000)  * 0.30
    if tnct > 100_000_000: t += (tnct - 100_000_000) * 0.35
    return int(t)

def fmt(n): return f"{int(n):,}".replace(",", ".")

def read_data(filepath):
    wb = openpyxl.load_workbook(filepath, data_only=True)
    all_rows = []
    for sname in wb.sheetnames:
        ws = wb[sname]
        rows = list(ws.iter_rows(values_only=True))
        header_idx = None
        for i, row in enumerate(rows):
            cells = " ".join(str(c or "").lower() for c in row)
            if ("họ tên" in cells or "ho ten" in cells) and (
                "thu nhập" in cells or "thu nhap" in cells or "số tiền" in cells):
                header_idx = i; break
        if header_idx is None: continue
        headers = [str(c or "").strip() for c in rows[header_idx]]
        for row in rows[header_idx+1:]:
            if not any(c for c in row if c not in (None, "", 0)): continue
            rec = {headers[j]: row[j] for j in range(min(len(headers), len(row)))}
            rec["_sheet"] = sname
            all_rows.append(rec)
    return all_rows

def aggregate(all_rows):
    def gv(rec, *keys):
        for k in keys:
            for hk in rec:
                if k.lower() in hk.lower():
                    v = parse_vnd(rec[hk])
                    if v: return v
        return 0

    def gs(rec, *keys):
        for k in keys:
            for hk in rec:
                if k.lower() in hk.lower():
                    v = str(rec[hk] or "").strip()
                    if v and v not in ("0", "None"): return v
        return ""

    periods = defaultdict(lambda: {
        "tn":0,"thue_kt":0,"bhxh":0,"cd":0,"gtgc":0,"has_bhxh":False
    })
    for rec in all_rows:
        name = str(next((rec[h] for h in rec if "họ" in h.lower()
                         or "ho ten" in h.lower()), "") or "").strip()
        if not name: continue
        period = gs(rec,"tháng trả lương","thang tra luong","tháng","thang") or "default"
        key = (name, period)
        bhxh = gv(rec,"BHXH khấu trừ","bhxh")
        gtgc = gv(rec,"Giảm trừ gia cảnh","giam tru gia canh","giam tru")
        periods[key]["tn"]      += gv(rec,"Tổng thu nhập","tong thu nhap","Số tiền","so tien")
        periods[key]["thue_kt"] += gv(rec,"Thuế TNCN đã khấu trừ","thue tncn da khau tru","Thuế TNCN","thue tncn")
        periods[key]["bhxh"]    += bhxh
        periods[key]["cd"]      += gv(rec,"Công đoàn","cong doan")
        periods[key]["gtgc"]    += gtgc
        if bhxh > 0: periods[key]["has_bhxh"] = True

    nv = defaultdict(lambda: {
        "tn":0,"thue_kt":0,"bhxh":0,"cd":0,"gtgc":0,"has_bhxh":False,"n_ky":0
    })
    for (name, period), d in periods.items():
        nv[name]["tn"]      += d["tn"]
        nv[name]["thue_kt"] += d["thue_kt"]
        nv[name]["bhxh"]    += d["bhxh"]
        nv[name]["cd"]      += d["cd"]
        nv[name]["gtgc"]    += d["gtgc"]
        if d["has_bhxh"]: nv[name]["has_bhxh"] = True
        if period != "default": nv[name]["n_ky"] += 1
    return nv

def build_report(nv, filepath):
    pl01 = {n:d for n,d in nv.items() if d["has_bhxh"]}
    pl02 = {n:d for n,d in nv.items() if not d["has_bhxh"]}

    results = {}
    for name, d in nv.items():
        tnct    = max(0, d["tn"] - d["bhxh"] - d["cd"] - d["gtgc"])
        pt      = calc_thue(tnct)
        cl      = pt - d["thue_kt"]
        n_ky    = max(d["n_ky"], 1)
        tnct_tb = tnct / n_ky
        results[name] = {**d, "tnct": tnct, "thue_pt": pt, "chenh_lech": cl, "tnct_tb": tnct_tb}

    bac = [0]*5
    for r in results.values():
        tb = r["tnct_tb"]
        if tb <= 0:         bac[0] += 1
        elif tb <= 10e6:    bac[1] += 1
        elif tb <= 30e6:    bac[2] += 1
        elif tb <= 60e6:    bac[3] += 1
        else:               bac[4] += 1

    t_tn   = sum(d["tn"]      for d in nv.values())
    t_bhxh = sum(d["bhxh"]    for d in nv.values())
    t_kt   = sum(d["thue_kt"] for d in nv.values())
    t_pt   = sum(r["thue_pt"] for r in results.values())
    cl_tong = t_pt - t_kt

    top3   = sorted(results.items(), key=lambda x: -x[1]["thue_pt"])[:3]
    bot3   = sorted(results.items(), key=lambda x:  x[1]["tn"])[:3]
    canh_bao = sorted(
        [(n,r) for n,r in results.items() if abs(r["chenh_lech"]) > 5_000_000],
        key=lambda x: -abs(x[1]["chenh_lech"])
    )

    SEP = "=" * 65
    lines = [
        SEP,
        "  TNCN-REVIEW -- Tong quan quyet toan thue TNCN",
        f"  Luat ap dung: Luat 109/2025/QH15",
        f"  File du lieu: {filepath}",
        f"  Ngay tao    : {datetime.now().strftime('%d/%m/%Y %H:%M')}",
        SEP,
        "",
        "A. TONG QUAN NHAN SU",
        f"  Tong nhan vien          : {len(nv):>5}",
        f"  Co BHXH  (Phu luc 01)  : {len(pl01):>5}",
        f"  Khong BHXH (Phu luc 02): {len(pl02):>5}",
        "",
        "B. CHI SO TAI CHINH (VND)",
        f"  Tong thu nhap da chi tra  : {fmt(t_tn):>25}",
        f"  Tong BHXH da khau tru    : {fmt(t_bhxh):>25}",
        f"  Thue TNCN da khau tru    : {fmt(t_kt):>25}",
        f"  Thue TNCN phai nop (L109): {fmt(t_pt):>25}",
        f"  Chenh lech               : {fmt(cl_tong):>25}",
        f"    => {'Phai nop them' if cl_tong > 0 else 'Duoc hoan thue' if cl_tong < 0 else 'Du, khong phat sinh them'}",
        "",
        "C. PHAN BO BAC THUE (TNCT trung binh/ky)",
        f"  Khong phai nop  (TNCT <= 0)          : {bac[0]:>4} nguoi",
        f"  Bac 1           (TNCT <= 10 trieu)   : {bac[1]:>4} nguoi",
        f"  Bac 2           (TNCT 10-30 trieu)   : {bac[2]:>4} nguoi",
        f"  Bac 3           (TNCT 30-60 trieu)   : {bac[3]:>4} nguoi",
        f"  Bac 4-5         (TNCT > 60 trieu)    : {bac[4]:>4} nguoi",
        "",
        "D. TOP & BOTTOM",
        "  Top 3 nguoi dong thue nhieu nhat:",
    ]
    for i, (n, r) in enumerate(top3):
        lines.append(f"    {i+1}. {n:<38} {fmt(r['thue_pt']):>15} VND")
    lines += ["  3 nguoi co thu nhap thap nhat:"]
    for i, (n, r) in enumerate(bot3):
        lines.append(f"    {i+1}. {n:<38} {fmt(r['tn']):>15} VND")
    lines += [
        "",
        f"E. CANH BAO BAT THUONG (|chenh lech| > 5.000.000 VND) — {len(canh_bao)} truong hop",
    ]
    for n, r in canh_bao[:10]:
        dau = "+" if r["chenh_lech"] > 0 else ""
        lines.append(f"  - {n}")
        lines.append(f"      Da KT: {fmt(r['thue_kt']):>15}  |  Phai nop: {fmt(r['thue_pt']):>15}  |  CL: {dau}{fmt(r['chenh_lech'])}")
    lines += [
        "",
        SEP,
        "  De tao bo ho so quyet toan day du:",
        "  /tncn-generator  (tu file Excel)",
        "  /tncn-sheets-sync (tu Google Sheets)",
        SEP,
    ]
    return "\n".join(lines)

if __name__ == "__main__":
    filepath = sys.argv[1] if len(sys.argv) > 1 else "Form bảng thu nhập học Claude code.xlsx"
    all_rows = read_data(filepath)
    nv = aggregate(all_rows)
    report = build_report(nv, filepath)
    OUTPUT_DIR.mkdir(exist_ok=True)
    out = OUTPUT_DIR / f"tncn_review_{datetime.now().strftime('%Y-%m-%d')}.txt"
    with open(out, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"OK: {out}")
