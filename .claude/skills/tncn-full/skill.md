---
name: tncn-full
description: Chạy toàn bộ quy trình quyết toán TNCN: fetch Google Sheets → tạo tờ khai chính thức → báo cáo tổng hợp
---

## Mục đích
Thực hiện 3 skill liên tiếp chỉ bằng 1 lệnh. Dùng khi cần cập nhật toàn bộ output sau mỗi lần dữ liệu Google Sheets thay đổi.

## Cách dùng

Chạy bằng Bash:
```
python .claude/skills/tncn-full/scripts/run_all.py
```

## Các bước thực hiện

```
Bước 1 — tncn-sheets-sync
  Fetch 2 sheet từ Google Sheets → output/bang_luong_from_sheets.xlsx

Bước 2 — tncn-generator
  Đọc bang_luong_from_sheets.xlsx → điền mẫu 05/QTT-TNCN
  → output/QuyetToanTNCN_{YYYY}.xls

Bước 3 — tncn-review
  Đọc bang_luong_from_sheets.xlsx → báo cáo tổng hợp nhanh
  → output/tncn_review_{YYYY-MM-DD}.xlsx
```

## Output sau khi chạy

| File | Mô tả |
|------|-------|
| `output/bang_luong_from_sheets.xlsx` | Dữ liệu thô từ Google Sheets |
| `output/QuyetToanTNCN_{YYYY}.xls` | Tờ khai quyết toán chính thức 05/QTT-TNCN |
| `output/tncn_review_{YYYY-MM-DD}.xlsx` | Báo cáo tổng hợp nhanh |
| `output/chat_history_*.txt` | Lịch sử chạy |
