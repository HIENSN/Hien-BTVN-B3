"""
Fetch income data from both Google Sheets and save as CSV files.
Run: python .claude/skills/tncn-sheets-sync/scripts/fetch_and_update.py
"""
import json
import csv
import sys
from pathlib import Path

CONFIG_PATH = Path(".claude/skills/tncn-sheets-sync/config.json")


def load_config():
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return json.load(f)


def get_sheets_service(credentials_file):
    try:
        from googleapiclient.discovery import build
        from google.oauth2.service_account import Credentials
    except ImportError:
        print("ERROR: Chạy lệnh sau để cài thư viện:")
        print("  pip install google-api-python-client google-auth")
        sys.exit(1)

    if not Path(credentials_file).exists():
        print(f"ERROR: Không tìm thấy credentials tại '{credentials_file}'")
        print("Xem hướng dẫn trong config.json")
        sys.exit(1)

    scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
    creds = Credentials.from_service_account_file(credentials_file, scopes=scopes)
    return build("sheets", "v4", credentials=creds)


def fetch_sheet(service, spreadsheet_id, range_name, output_path):
    result = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=spreadsheet_id, range=range_name)
        .execute()
    )
    rows = result.get("values", [])

    if not rows:
        print(f"WARNING: Sheet '{range_name}' trống.")
        return 0

    Path(output_path).parent.mkdir(exist_ok=True)
    with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    data_rows = len(rows) - 1
    print(f"OK: {range_name} → {output_path} ({data_rows} dòng dữ liệu)")
    return data_rows


if __name__ == "__main__":
    config = load_config()

    if config["spreadsheet_id"] == "YOUR_SPREADSHEET_ID_HERE":
        print("ERROR: Chưa điền spreadsheet_id trong config.json")
        sys.exit(1)

    print(f"Kết nối Google Sheets: {config['spreadsheet_id']}")
    service = get_sheets_service(config["credentials_file"])

    count1 = fetch_sheet(
        service,
        config["spreadsheet_id"],
        config["sheet1_range"],
        f"{config['output_dir']}/temp_sheet1.csv"
    )
    count2 = fetch_sheet(
        service,
        config["spreadsheet_id"],
        config["sheet2_range"],
        f"{config['output_dir']}/temp_sheet2.csv"
    )

    print(f"\nHoàn thành. Tổng cộng {count1 + count2} dòng từ 2 sheet.")
    print("Tiếp theo: Claude sẽ xử lý dữ liệu và tạo hồ sơ quyết toán TNCN.")
