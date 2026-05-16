"""
Skill 1 - tncn-generator
Doc file Excel nhieu sheet bang luong, tinh thue TNCN theo Luat 109/2025/QH15,
dien vao mau chinh thuc 05/QTT-TNCN va xuat file ket qua.

Cach dung:
    python .claude/skills/tncn-generator/scripts/generate_tncn.py <bang_luong.xlsx>
"""
import sys, io, shutil
from datetime import datetime
from collections import defaultdict
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

try:
    import xlrd
    from xlutils.copy import copy as xl_copy
    import xlwt
except ImportError:
    print("ERROR: pip install xlrd xlutils xlwt openpyxl")
    sys.exit(1)

try:
    import openpyxl
except ImportError:
    openpyxl = None

# ── Thue Luat 109/2025/QH15 ───────────────────────────────────────────────────
GIAM_TRU_BAN_THAN  = 15_500_000
GIAM_TRU_PHU_THUOC = 6_200_000
TEMPLATE = Path("05_QTT_TNCN_TT80_2025.xls")
OUTPUT_DIR = Path("output")

def parse_vnd(v):
    if v is None: return 0
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

# ── Doc tat ca sheet tu file dau vao ─────────────────────────────────────────
def read_input(filepath):
    ext = Path(filepath).suffix.lower()
    all_rows = []
    INCOME_KEYWORDS = {
        "ho ten", "ho va ten", "tong thu nhap", "thue tncn",
        "họ tên", "họ và tên", "tổng thu nhập", "thuế tncn"
    }

    def process_rows(rows_iter, sheet_name):
        rows = list(rows_iter)
        header_idx = None
        for i, row in enumerate(rows):
            cells = [str(c).lower().strip() if c else "" for c in row]
            combined = " ".join(cells)
            if sum(1 for k in INCOME_KEYWORDS if k in combined) >= 2:
                header_idx = i
                break
        if header_idx is None:
            return 0
        headers = [str(c).strip() if c else "" for c in rows[header_idx]]
        count = 0
        for row in rows[header_idx + 1:]:
            if not any(c for c in row if c not in (None, "", 0)):
                continue
            rec = {headers[j]: row[j] for j in range(min(len(headers), len(row)))}
            name = str(rec.get("Ho ten", rec.get("Ho va ten",
                   rec.get("Họ tên", rec.get("Họ và tên", "")))) or "").strip()
            if not name:
                continue
            rec["_sheet"] = sheet_name
            all_rows.append(rec)
            count += 1
        return count

    if ext == ".csv":
        import csv as _csv
        with open(filepath, encoding="utf-8-sig") as f:
            rows_csv = list(_csv.reader(f))
        n = process_rows(iter(rows_csv), Path(filepath).stem)
        if n: print(f"  File CSV '{Path(filepath).name}': {n} dong")
    elif ext == ".xls":
        wb_xls = xlrd.open_workbook(filepath)
        for sname in wb_xls.sheet_names():
            ws = wb_xls.sheet_by_name(sname)
            rows_iter = ([ws.cell_value(r, c) for c in range(ws.ncols)] for r in range(ws.nrows))
            n = process_rows(rows_iter, sname)
            if n: print(f"  Sheet '{sname}': {n} dong")
    elif ext in (".xlsx", ".xlsm") and openpyxl:
        wb_px = openpyxl.load_workbook(filepath, data_only=True)
        for sname in wb_px.sheetnames:
            ws = wb_px[sname]
            rows_iter = ([c.value for c in row] for row in ws.iter_rows())
            n = process_rows(rows_iter, sname)
            if n: print(f"  Sheet '{sname}': {n} dong")
    else:
        print(f"ERROR: Dinh dang khong ho tro: {ext}")
        sys.exit(1)

    return all_rows

# ── Tong hop theo nhan vien ───────────────────────────────────────────────────
def aggregate(all_rows):
    nv = defaultdict(lambda: {
        "tn":0, "thue_kt":0, "bhxh":0, "cd":0, "gtgc":0,
        "npt":0, "cccd":"", "mst":"", "has_bhxh":False
    })

    def gv(rec, *keys):
        for k in keys:
            for hk in rec:
                if k.lower() in hk.lower():
                    return parse_vnd(rec[hk])
        return 0

    def gs(rec, *keys):
        for k in keys:
            for hk in rec:
                if k.lower() in hk.lower():
                    v = str(rec[hk] or "").strip()
                    if v and v != "0": return v
        return ""

    for rec in all_rows:
        name = str(rec.get("Ho ten", rec.get("Ho va ten",
               rec.get("Họ tên", rec.get("Họ và tên", "")))) or "").strip()
        if not name: continue

        bhxh = gv(rec, "BHXH khau tru", "bhxh")
        gtgc = gv(rec, "Giam tru gia canh", "giam tru")
        if gtgc == 0: gtgc = GIAM_TRU_BAN_THAN

        nv[name]["tn"]      += gv(rec, "Tổng thu nhập", "Tong thu nhap", "Số tiền", "So tien")
        nv[name]["thue_kt"] += gv(rec, "Thuế TNCN đã khấu trừ", "Thue TNCN da khau tru", "Thuế TNCN", "Thue TNCN")
        nv[name]["bhxh"]    += bhxh
        nv[name]["cd"]      += gv(rec, "Cong doan")
        nv[name]["gtgc"]    += gtgc
        if bhxh > 0: nv[name]["has_bhxh"] = True
        if not nv[name]["cccd"]: nv[name]["cccd"] = gs(rec, "cccd", "cmnd", "so cccd")
        if not nv[name]["mst"]:  nv[name]["mst"]  = gs(rec, "ma so thue", "mst")

    return nv

# ── Ghi vao mau .xls ─────────────────────────────────────────────────────────
def write_to_template(nv, year, output_path):
    rb = xlrd.open_workbook(str(TEMPLATE), formatting_info=True)
    wb = xl_copy(rb)

    pl01 = {n:d for n,d in nv.items() if d["has_bhxh"]}
    pl02 = {n:d for n,d in nv.items() if not d["has_bhxh"]}

    t_tn   = sum(d["tn"]      for d in nv.values())
    t_kt   = sum(d["thue_kt"] for d in nv.values())
    t_pt   = sum(calc_thue(max(0, d["tn"]-d["bhxh"]-d["cd"]-d["gtgc"])) for d in nv.values())
    t_bhxh = sum(d["bhxh"]    for d in nv.values())

    def ws(name): return wb.get_sheet(rb.sheet_names().index(name))
    def w(sheet, r, c, v): sheet.write(r, c, v)

    # ── To khai chinh ──────────────────────────────────────────────────────
    tk = ws("Tờ khai")
    w(tk,  2, 10, f"Kỳ tính thuế:  Năm {year}")
    w(tk, 47, 20, len(nv))           # [16] Tong nguoi lao dong
    w(tk, 48, 20, len(pl01))         # [17] Co hop dong
    w(tk, 49, 20, len(nv))           # [18] Da khau tru
    w(tk, 50, 20, len(nv))           # [19] Cu tru
    w(tk, 51, 20, 0)                 # [20] Khong cu tru
    w(tk, 59, 20, t_tn)              # [23] Tong TNCT
    w(tk, 60, 20, t_tn)              # [24] Cu tru
    w(tk, 61, 20, 0)                 # [25] Khong cu tru

    # Tim row chua tong thue (doc tiep de map chinh xac)
    for row_idx in range(62, rb.sheet_by_name("Tờ khai").nrows):
        cell_val = str(rb.sheet_by_name("Tờ khai").cell_value(row_idx, 2))
        if "khấu trừ" in cell_val.lower() and "tổng" in cell_val.lower():
            w(tk, row_idx, 20, t_kt)
            break
    for row_idx in range(62, rb.sheet_by_name("Tờ khai").nrows):
        cell_val = str(rb.sheet_by_name("Tờ khai").cell_value(row_idx, 2))
        if "phải nộp" in cell_val.lower() and "tổng" in cell_val.lower():
            w(tk, row_idx, 20, t_pt)
            break

    # ── Phu luc 01 ────────────────────────────────────────────────────────
    pl01_ws = ws("05-1_BK-TNCN")
    w(pl01_ws, 4, 12, f"Kỳ tính thuế:  Năm {year}")
    data_start = 23
    for i, (name, d) in enumerate(sorted(pl01.items())):
        r = data_start + i
        tnct = max(0, d["tn"] - d["bhxh"] - d["cd"] - d["gtgc"])
        pt   = calc_thue(tnct)
        cl   = pt - d["thue_kt"]
        w(pl01_ws, r,  1, i+1)           # STT [06]
        w(pl01_ws, r,  3, name)          # Ho ten [07]
        w(pl01_ws, r,  4, d["mst"])      # MST [08]
        w(pl01_ws, r,  7, d["cccd"])     # CCCD [09]
        w(pl01_ws, r, 12, d["tn"])       # TNCT [12]
        w(pl01_ws, r, 26, d["bhxh"])     # BHXH [19]
        w(pl01_ws, r, 22, d["gtgc"])     # Giam tru GC [17]
        w(pl01_ws, r, 30, tnct)          # TN tinh thue [21]
        w(pl01_ws, r, 32, d["thue_kt"])  # Thue da KT [22]
        w(pl01_ws, r, 36, pt)            # Thue phai nop [24]
        if cl < 0: w(pl01_ws, r, 38, abs(cl))   # Thue nop thua [25]
        if cl > 0: w(pl01_ws, r, 40, cl)         # Thue con phai nop [26]

    # ── Phu luc 02 ────────────────────────────────────────────────────────
    pl02_ws = ws("05-2_BK-TNCN")
    w(pl02_ws, 4, 12, f"Kỳ tính thuế:  Năm {year}")
    for i, (name, d) in enumerate(sorted(pl02.items())):
        r = data_start + i
        tnct = max(0, d["tn"] - d["gtgc"])
        pt   = calc_thue(tnct)
        cl   = pt - d["thue_kt"]
        w(pl02_ws, r,  1, i+1)
        w(pl02_ws, r,  3, name)
        w(pl02_ws, r,  4, d["mst"])
        w(pl02_ws, r,  7, d["cccd"])
        w(pl02_ws, r, 10, d["tn"])
        w(pl02_ws, r, 32, d["thue_kt"])
        w(pl02_ws, r, 36, pt)
        if cl < 0: w(pl02_ws, r, 38, abs(cl))
        if cl > 0: w(pl02_ws, r, 40, cl)

    wb.save(str(output_path))

# ── Chat history ─────────────────────────────────────────────────────────────
def write_chat_history(nv, input_file, output_path, year):
    pl01 = {n:d for n,d in nv.items() if d["has_bhxh"]}
    pl02 = {n:d for n,d in nv.items() if not d["has_bhxh"]}
    t_tn = sum(d["tn"] for d in nv.values())
    t_kt = sum(d["thue_kt"] for d in nv.values())
    t_pt = sum(calc_thue(max(0,d["tn"]-d["bhxh"]-d["cd"]-d["gtgc"])) for d in nv.values())

    def fmt(n): return f"{int(n):,}".replace(",",".")

    lines = [
        "=" * 60,
        "  CLAUDE CODE CHAT HISTORY — tncn-generator",
        "=" * 60,
        f"Thoi gian    : {datetime.now().strftime('%d/%m/%Y %H:%M')}",
        f"Skill        : tncn-generator",
        f"File dau vao : {input_file}",
        f"Luat thue    : Luat 109/2025/QH15",
        f"Nam tinh thue: {year}",
        "",
        "KET QUA XU LY:",
        f"  Phu luc 01 (co BHXH)     : {len(pl01):>5} nguoi",
        f"  Phu luc 02 (khong BHXH)  : {len(pl02):>5} nguoi",
        f"  Tong nhan su             : {len(nv):>5} nguoi",
        "",
        "CHI SO TAI CHINH:",
        f"  Tong thu nhap da tra  : {fmt(t_tn):>20} VND",
        f"  Thue TNCN da khau tru : {fmt(t_kt):>20} VND",
        f"  Thue TNCN phai nop    : {fmt(t_pt):>20} VND",
        f"  Chenh lech            : {fmt(t_pt-t_kt):>20} VND",
        "",
        "FILE DA TAO:",
        f"  {output_path}",
        "    Sheet: To khai chinh (05/QTT-TNCN)",
        f"    Sheet: Phu luc 01 — 05-1/BK-TNCN ({len(pl01)} nguoi co BHXH)",
        f"    Sheet: Phu luc 02 — 05-2/BK-TNCN ({len(pl02)} nguoi khong BHXH)",
        "    Sheet: Phu luc 03 — 05-3/BK-TNCN (de trong)",
        "=" * 60,
    ]

    hist_path = OUTPUT_DIR / f"chat_history_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.txt"
    with open(hist_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  Chat history: {hist_path}")

# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Cach dung: python generate_tncn.py <duong_dan_file_bang_luong>")
        print("Vi du   : python generate_tncn.py bang_luong_2026.xlsx")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"ERROR: Khong tim thay file '{input_path}'")
        sys.exit(1)

    if not TEMPLATE.exists():
        print(f"ERROR: Khong tim thay mau '{TEMPLATE}'")
        print("Dam bao file 05_QTT_TNCN_TT80_2025.xls nam cung thu muc chay script.")
        sys.exit(1)

    year = datetime.now().year
    OUTPUT_DIR.mkdir(exist_ok=True)
    output_path = OUTPUT_DIR / f"QuyetToanTNCN_{year}.xls"

    print(f"Doc du lieu: {input_path}")
    all_rows = read_input(str(input_path))
    print(f"Tong {len(all_rows)} dong tu tat ca sheet")

    print("Tong hop theo nhan vien...")
    nv = aggregate(all_rows)
    pl01 = {n:d for n,d in nv.items() if d["has_bhxh"]}
    pl02 = {n:d for n,d in nv.items() if not d["has_bhxh"]}
    print(f"  {len(nv)} nhan vien: {len(pl01)} co BHXH (PL01), {len(pl02)} khong BHXH (PL02)")

    print(f"Dien vao mau chinh thuc...")
    write_to_template(nv, year, output_path)

    write_chat_history(nv, input_path, output_path, year)

    print(f"\nHoan thanh!")
    print(f"  Output: {output_path}")
    print(f"  Mo file bang Excel de kiem tra.")
