---
name: tncn-sheets-sync
description: Kết nối Google Sheets công khai, tải dữ liệu bảng lương thô về file Excel để Skill 1 và Skill 3 xử lý
---

## Mục đích
Đồng bộ dữ liệu mới nhất từ Google Sheets về máy local dưới dạng file Excel thô.
Mỗi lần chạy lại sẽ ghi đè file cũ → Skill 1 và Skill 3 luôn đọc dữ liệu mới nhất.

## Yêu cầu duy nhất
Google Sheet phải được share **"Anyone with the link → Viewer"**. Không cần API key hay credentials.

## Cách dùng

### Bước 1 — Fetch và lưu dữ liệu thô
Chạy script bằng Bash:
```
python .claude/skills/tncn-sheets-sync/scripts/fetch_and_update.py
```

Script tải 2 sheet từ Google Sheets, gộp vào một file Excel duy nhất:
```
output/bang_luong_from_sheets.xlsx
  └── Sheet "Tổng thu nhập"   (nhân viên có BHXH)
  └── Sheet "CTV"             (cộng tác viên)
```

File này có cùng cấu trúc với file bảng lương thực tế, dùng được trực tiếp với Skill 1 và Skill 3.

### Bước 2 — Thông báo kết quả
Hiển thị:
- Số dòng mỗi sheet
- Đường dẫn file đã lưu
- Gợi ý bước tiếp theo

## Flow đầy đủ
```
Google Sheets  ──►  /tncn-sheets-sync  ──►  output/bang_luong_from_sheets.xlsx
                                                        │
                                    ┌───────────────────┴──────────────────┐
                                    ▼                                      ▼
                             /tncn-generator                         /tncn-review
                         QuyetToanTNCN_2026.xls              tncn_review_YYYY-MM-DD.xlsx
```

Mỗi khi Google Sheets thay đổi: chạy lại `/tncn-sheets-sync` → chạy lại `/tncn-generator` và/hoặc `/tncn-review` để có output cập nhật.
