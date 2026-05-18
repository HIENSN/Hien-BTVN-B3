---
name: tncn-generator
description: Đọc file Excel bảng lương, phân loại nhân sự, tính thuế TNCN theo Luật 109/2025/QH15 và xuất bộ hồ sơ quyết toán 05/QTT-TNCN đầy đủ
---

## Mục đích
Từ file Excel bảng lương (có thể từ nhiều sheet), tự động điền vào mẫu chính thức
`05_QTT_TNCN_TT80_2025.xls` và xuất file quyết toán hoàn chỉnh.

---

## QUY ĐỊNH THUẾ ÁP DỤNG — Luật 109/2025/QH15 (hiệu lực 01/07/2026)

### Giảm trừ gia cảnh
- Bản thân người nộp thuế: **15.500.000 VND/tháng**
- Mỗi người phụ thuộc: **6.200.000 VND/tháng**

### Biểu thuế lũy tiến từng phần (cá nhân cư trú)
| Bậc | Thu nhập chịu thuế/tháng | Thuế suất |
|-----|--------------------------|-----------|
| 1 | Đến 10 triệu | 5% |
| 2 | Trên 10 – 30 triệu | 10% |
| 3 | Trên 30 – 60 triệu | 20% |
| 4 | Trên 60 – 100 triệu | 30% |
| 5 | Trên 100 triệu | 35% |

---

## CÁC BƯỚC THỰC HIỆN

### Bước 1 — Nhận file đầu vào
Yêu cầu người dùng cung cấp đường dẫn file Excel (.xlsx hoặc .xls).

**Nếu đã chạy `/tncn-sheets-sync` trước đó**, mặc định dùng:
```
output/bang_luong_from_sheets.xlsx
```

Chạy bằng Bash:
```
python .claude/skills/tncn-generator/scripts/generate_tncn.py "output/bang_luong_from_sheets.xlsx"
```

Đảm bảo file mẫu `05_QTT_TNCN_TT80_2025.xls` nằm trong thư mục gốc project.

### Bước 2 — Phân loại từng dòng
- `BHXH khấu trừ > 0` → **Phụ lục 01** (có hợp đồng lao động)
- `BHXH khấu trừ = 0 hoặc trống` → **Phụ lục 02** (không có hợp đồng)

### Bước 3 — Tổng hợp theo từng người
Group theo (Họ tên, Tháng trả lương), cộng dồn thu nhập và khấu trừ, lấy Giảm trừ gia cảnh từ cột dữ liệu nguồn (cộng thẳng giá trị có sẵn).

### Bước 4 — Điền vào mẫu chính thức
Điền số liệu vào `05_QTT_TNCN_TT80_2025.xls`, xuất ra:
```
output/QuyetToanTNCN_{YYYY}.xls
```

### Bước 5 — Xuất chat history
```
output/chat_history_{YYYY-MM-DD_HH-MM}.txt
```
