"""
Skill 4 - tncn-full
Chay tuan tu ca 3 skill: tncn-sheets-sync -> tncn-generator -> tncn-review
"""
import sys, io, subprocess
from datetime import datetime
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

INPUT_FILE = "output/bang_luong_from_sheets.xlsx"
SEP = "=" * 60

def run(label, cmd):
    print(f"\n{SEP}")
    print(f"  {label}")
    print(SEP)
    result = subprocess.run(
        [sys.executable] + cmd,
        capture_output=True, text=True, encoding="utf-8"
    )
    if result.stdout: print(result.stdout.strip())
    if result.stderr: print(result.stderr.strip())
    if result.returncode != 0:
        print(f"\nERROR: {label} that bai (exit code {result.returncode})")
        sys.exit(result.returncode)

if __name__ == "__main__":
    start = datetime.now()
    print(f"\n{'=' * 60}")
    print(f"  TNCN-FULL — Chay toan bo quy trinh quyet toan TNCN")
    print(f"  Bat dau: {start.strftime('%d/%m/%Y %H:%M')}")
    print(f"{'=' * 60}")

    run(
        "BUOC 1/3 — tncn-sheets-sync: Fetch du lieu tu Google Sheets",
        [".claude/skills/tncn-sheets-sync/scripts/fetch_and_update.py"]
    )

    run(
        "BUOC 2/3 — tncn-generator: Tao To khai quyet toan chinh thuc",
        [".claude/skills/tncn-generator/scripts/generate_tncn.py", INPUT_FILE]
    )

    run(
        "BUOC 3/3 — tncn-review: Tao bao cao tong hop nhanh",
        [".claude/skills/tncn-review/scripts/review_tncn.py", INPUT_FILE]
    )

    elapsed = (datetime.now() - start).seconds
    print(f"\n{SEP}")
    print(f"  HOAN THANH — {elapsed}s")
    print(f"  output/bang_luong_from_sheets.xlsx   (du lieu tho)")
    print(f"  output/QuyetToanTNCN_{datetime.now().year}.xls       (to khai chinh thuc)")
    print(f"  output/tncn_review_{datetime.now().strftime('%Y-%m-%d')}.xlsx (bao cao tong hop)")
    print(SEP)
