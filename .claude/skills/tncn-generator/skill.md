---
name: tncn-generator
description: Đọc file CSV bảng lương, phân loại nhân sự, tính thuế TNCN theo Luật 109/2025/QH15 và xuất bộ hồ sơ quyết toán 05/QTT-TNCN đầy đủ
---

## Mục đích
Từ file CSV bảng lương thực tế (có thể từ nhiều sheet), tự động tạo bộ hồ sơ quyết toán thuế TNCN gồm Tờ khai chính + 3 Phụ lục theo Thông tư 80/2021/TT-BTC.

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

### Công thức tính thuế lũy tiến (tháng)
```
Bậc 1: min(TNCT, 10M) × 5%
Bậc 2: min(max(TNCT - 10M, 0), 20M) × 10%
Bậc 3: min(max(TNCT - 30M, 0), 30M) × 20%
Bậc 4: min(max(TNCT - 60M, 0), 40M) × 30%
Bậc 5: max(TNCT - 100M, 0) × 35%
Tổng thuế = Bậc 1 + Bậc 2 + Bậc 3 + Bậc 4 + Bậc 5
```

---

## CÁC BƯỚC THỰC HIỆN

### Bước 1 — Nhận file đầu vào
Yêu cầu người dùng cung cấp đường dẫn file CSV. Nếu có 2 file (2 sheet xuất riêng), đọc cả hai và gộp lại.
Đọc bằng Bash: `cat "{đường_dẫn}"`

Các cột có thể gặp trong CSV:
- `Tháng trả lương` — VD: Tháng 1
- `Họ tên`
- `Tổng thu nhập` — thu nhập gộp (VND)
- `Thuế TNCN đã khấu trừ` — thuế đã khấu trừ tại nguồn
- `Loại thu nhập` — Lương cứng / Thưởng...
- `Hình thức chi`
- `Lương đóng BHXH`
- `BHXH khấu trừ` — phần nhân viên đóng BHXH+BHYT+BHTN
- `Công đoàn khấu trừ`
- `Giảm trừ gia cảnh` — nếu có, dùng giá trị này; nếu không có, mặc định 15.500.000

### Bước 2 — Phân loại từng dòng
- `BHXH khấu trừ > 0` → **Phụ lục 01** (có hợp đồng lao động)
- `BHXH khấu trừ = 0 hoặc trống` → **Phụ lục 02** (không có hợp đồng)

### Bước 3 — Tổng hợp theo từng người (cộng dồn tất cả tháng)
Với mỗi nhân viên, tính:
```
Thu nhập chịu thuế/tháng = Tổng thu nhập - BHXH khấu trừ - Công đoàn - Giảm trừ gia cảnh
Thuế TNCN phải nộp      = tính lũy tiến 5 bậc (xem công thức trên)
Chênh lệch              = Thuế phải nộp - Thuế đã khấu trừ
  > 0: còn nộp thêm | < 0: được hoàn thuế | = 0: đủ
```

### Bước 4 — Tạo 4 file output
Đọc template tương ứng trong `.claude/skills/tncn-generator/templates/`, điền số liệu, ghi ra `output/`:

| File output | Template | Nội dung |
|-------------|----------|---------|
| `output/05_QTT-TNCN_{YYYY}.txt` | `to_khai_chinh.txt` | Tờ khai tổng hợp |
| `output/05-1_BK-QTT-TNCN_{YYYY}.txt` | `phu_luc_01.txt` | Danh sách có BHXH |
| `output/05-2_BK-QTT-TNCN_{YYYY}.txt` | `phu_luc_02.txt` | Danh sách không BHXH |
| `output/05-3_BK-QTT-TNCN_{YYYY}.txt` | `phu_luc_03.txt` | Người phụ thuộc (để trống) |

### Bước 5 — Xuất chat history
Tạo file `output/chat_history_{YYYY-MM-DD_HH-MM}.txt` ghi lại:
- Thời gian chạy skill và file đầu vào
- Bảng tóm tắt từng nhân viên: họ tên | tháng | thu nhập | thuế đã khấu trừ | thuế phải nộp | chênh lệch
- Tổng số phụ lục đã tạo và đường dẫn từng file
