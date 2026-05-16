"""
Fetch income data from public Google Sheets and save as CSV files.
No credentials required — sheet must be shared as "Anyone with the link".
Run: python .claude/skills/tncn-sheets-sync/scripts/fetch_and_update.py
"""
import json
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

try:
    import urllib.request
except ImportError:
    print("ERROR: urllib not available")
    sys.exit(1)

CONFIG_PATH = Path(".claude/skills/tncn-sheets-sync/config.json")


def load_config():
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return json.load(f)


def fetch_sheet_as_csv(spreadsheet_id, gid, output_path):
    url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv&gid={gid}"
    print(f"Đang tải: gid={gid} ...")

    try:
        with urllib.request.urlopen(url) as response:
            if response.status != 200:
                print(f"ERROR: HTTP {response.status}")
                return 0
            content = response.read().decode("utf-8-sig")
    except Exception as e:
        print(f"ERROR: Không tải được sheet (gid={gid}): {e}")
        print("Kiểm tra lại: sheet đã được share 'Anyone with the link'?")
        return 0

    Path(output_path).parent.mkdir(exist_ok=True)
    with open(output_path, "w", encoding="utf-8-sig") as f:
        f.write(content)

    rows = content.strip().split("\n")
    data_rows = len(rows) - 1
    print(f"OK: {data_rows} dòng dữ liệu → {output_path}")
    return data_rows


if __name__ == "__main__":
    config = load_config()
    sid = config["spreadsheet_id"]
    out = config["output_dir"]

    print(f"Spreadsheet ID: {sid}")

    count1 = fetch_sheet_as_csv(sid, config["sheet1_gid"], f"{out}/temp_sheet1.csv")
    count2 = fetch_sheet_as_csv(sid, config["sheet2_gid"], f"{out}/temp_sheet2.csv")

    print(f"\nHoàn thành. Tổng {count1 + count2} dòng từ 2 sheet.")
    print("Claude sẽ xử lý dữ liệu và tạo hồ sơ quyết toán TNCN.")
