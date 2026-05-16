---
name: tncn-sheets-sync
description: Kết nối Google Sheets API đọc 2 sheet bảng lương, tự động tạo lại bộ hồ sơ quyết toán TNCN theo Luật 109/2025/QH15 và xuất chat history
---

## Mục đích
Kéo dữ liệu mới nhất từ Google Sheets (2 sheet trong cùng 1 file), xử lý và tạo bộ hồ sơ quyết toán TNCN đầy đủ. Chạy lại bất cứ lúc nào để cập nhật theo dữ liệu mới nhất.

## Yêu cầu trước khi chạy
1. Đã điền `spreadsheet_id`, `sheet1_gid`, `sheet2_gid` trong config.json
2. Đã đặt file `credentials.json` (Google Service Account) vào thư mục này
3. Đã chia sẻ Google Sheet với email service account (quyền Viewer)
4. Python đã cài: `pip install google-api-python-client google-auth`

## Bước 1 — Fetch dữ liệu
Chạy script:
```
python .claude/skills/tncn-sheets-sync/scripts/fetch_and_update.py
```
Script tải Sheet 1 → `output/temp_sheet1.csv` và Sheet 2 → `output/temp_sheet2.csv`.

## Bước 2 — Xử lý và phân loại
Đọc cả 2 file temp, gộp dữ liệu, phân loại:
- `BHXH khấu trừ > 0` → Phụ lục 01
- `BHXH khấu trừ = 0 hoặc trống` → Phụ lục 02

## Bước 3 — Tính thuế theo Luật 109/2025/QH15
Giảm trừ bản thân: **15.500.000 VND/tháng**
Giảm trừ người phụ thuộc: **6.200.000 VND/người/tháng**

Biểu thuế 5 bậc:
| Bậc | Thu nhập chịu thuế/tháng | Thuế suất |
|-----|--------------------------|-----------|
| 1 | Đến 10 triệu | 5% |
| 2 | Trên 10 – 30 triệu | 10% |
| 3 | Trên 30 – 60 triệu | 20% |
| 4 | Trên 60 – 100 triệu | 30% |
| 5 | Trên 100 triệu | 35% |

## Bước 4 — Tạo output
Ghi ra thư mục `output/`:
```
05_QTT-TNCN_{YYYY}.txt
05-1_BK-QTT-TNCN_{YYYY}.txt
05-2_BK-QTT-TNCN_{YYYY}.txt
05-3_BK-QTT-TNCN_{YYYY}.txt
chat_history_{YYYY-MM-DD_HH-MM}.txt
```

## Bước 5 — Báo cáo thay đổi trong chat
So với lần chạy trước (nếu có), hiển thị:
- Nhân viên mới thêm / bị xóa
- Nhân viên có thay đổi số thuế
- Thời gian đồng bộ và số dòng đã xử lý
