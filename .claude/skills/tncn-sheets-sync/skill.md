---
name: tncn-sheets-sync
description: Kết nối Google Sheets công khai, tự động tạo bộ hồ sơ quyết toán TNCN theo Luật 109/2025/QH15 và xuất chat history
---

## Mục đích
Kéo dữ liệu mới nhất từ Google Sheets (2 sheet), xử lý và tạo bộ hồ sơ quyết toán TNCN đầy đủ. Chạy lại bất cứ lúc nào để cập nhật khi dữ liệu thay đổi.

## Yêu cầu duy nhất
Google Sheet phải được share **"Anyone with the link → Viewer"**. Không cần API key hay credentials.

## Bước 1 — Fetch dữ liệu
Chạy script bằng Bash:
```
python .claude/skills/tncn-sheets-sync/scripts/fetch_and_update.py
```
Script tải Sheet 1 → `output/temp_sheet1.csv` và Sheet 2 → `output/temp_sheet2.csv`.

## Bước 2 — Xử lý và phân loại
Đọc cả 2 file CSV vừa tải, gộp dữ liệu, phân loại:
- `BHXH khấu trừ > 0` → Phụ lục 01 (có hợp đồng lao động)
- `BHXH khấu trừ = 0 hoặc trống` → Phụ lục 02 (không có hợp đồng)

## Bước 3 — Tính thuế theo Luật 109/2025/QH15
Giảm trừ bản thân: **15.500.000 VND/tháng**
Giảm trừ người phụ thuộc: **6.200.000 VND/người/tháng**

Biểu thuế 5 bậc:
| Bậc | Thu nhập chịu thuế/tháng | Thuế suất |
|-----|--------------------------|-----------|
| 1   | Đến 10 triệu             | 5%        |
| 2   | Trên 10 – 30 triệu       | 10%       |
| 3   | Trên 30 – 60 triệu       | 20%       |
| 4   | Trên 60 – 100 triệu      | 30%       |
| 5   | Trên 100 triệu           | 35%       |

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
