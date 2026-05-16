---
name: tncn-review
description: Phân tích nhanh bảng lương, xuất file tổng quan thuế TNCN dạng .xlsx theo Luật 109/2025/QH15
---

## Mục đích
Xem nhanh tình hình thuế TNCN toàn bộ nhân sự mà không cần tạo hồ sơ đầy đủ.
Hữu ích để kiểm tra trước khi quyết toán hoặc phát hiện bất thường.

## Quy định áp dụng — Luật 109/2025/QH15
- Giảm trừ bản thân: 15.500.000 VND/tháng
- Giảm trừ người phụ thuộc: 6.200.000 VND/người/tháng
- Biểu thuế 5 bậc: 5% / 10% / 20% / 30% / 35%

## Cách dùng

### Bước 1 — Nhận file đầu vào
Yêu cầu người dùng cung cấp đường dẫn file Excel.

**Nếu đã chạy `/tncn-sheets-sync` trước đó**, mặc định dùng:
```
output/bang_luong_from_sheets.xlsx
```

### Bước 2 — Chạy script
```
python .claude/skills/tncn-review/scripts/review_tncn.py "output/bang_luong_from_sheets.xlsx"
```

### Bước 3 — Output
File được ghi ra (không hiển thị trong chat):
```
output/tncn_review_{YYYY-MM-DD}.xlsx
```

Nội dung gồm 5 mục:
- **A.** Tổng quan nhân sự (tổng, PL01, PL02)
- **B.** Chỉ số tài chính (tổng thu nhập, BHXH, thuế đã KT, thuế phải nộp, chênh lệch)
- **C.** Phân bổ bậc thuế theo TNCT trung bình/kỳ
- **D.** Top 3 đóng thuế nhiều nhất / 3 thu nhập thấp nhất
- **E.** Cảnh báo bất thường (chênh lệch > 5.000.000 VND)

## Flow kết hợp với các skill khác
```
/tncn-sheets-sync  →  output/bang_luong_from_sheets.xlsx
                              │
             ┌────────────────┴────────────────┐
             ▼                                 ▼
     /tncn-generator                    /tncn-review
  QuyetToanTNCN_2026.xls         tncn_review_YYYY-MM-DD.xlsx
```
