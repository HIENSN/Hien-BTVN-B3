---
name: tncn-personal-calc
description: Tính thuế TNCN cho 1 cá nhân — nhập thu nhập, BHXH, số người phụ thuộc → xuất kết quả chi tiết theo 5 bậc lũy tiến (Luật 109/2025/QH15)
---

## Mục đích
Tính thuế TNCN nhanh cho một cá nhân cụ thể, hiển thị breakdown theo từng bậc thuế.
Port trực tiếp từ logic JavaScript của Mini Tool `index.html`.

## Quy định áp dụng — Luật 109/2025/QH15 (từ 01/01/2026)

| Khoản giảm trừ | Tháng | Năm |
|---|---|---|
| Bản thân người nộp thuế | 15.500.000 đ | 186.000.000 đ |
| Mỗi người phụ thuộc | 6.200.000 đ | 74.400.000 đ |

| Bậc | Thu nhập tính thuế / năm | Thuế suất |
|---|---|---|
| 1 | Đến 120 triệu | 5% |
| 2 | Trên 120 – 360 triệu | 10% |
| 3 | Trên 360 – 720 triệu | 20% |
| 4 | Trên 720 – 1.200 triệu | 30% |
| 5 | Trên 1.200 triệu | 35% |

---

## Các bước thực hiện

### Bước 1 — Thu thập thông tin từ người dùng

Hỏi lần lượt (hoặc nhận từ câu hỏi ban đầu):
- **Tên người tính thuế** (tuỳ chọn)
- **Tổng thu nhập chịu thuế / năm** (VND) — có thể nhập nhiều nguồn, cộng lại
- **Bảo hiểm bắt buộc đã đóng / năm** (BHXH + BHYT + BHTN, mặc định 0 nếu không có)
- **Số người phụ thuộc** (mặc định 0)

> Nếu người dùng nhập thu nhập theo tháng → nhân 12 trước khi truyền vào script.

### Bước 2 — Chạy script tính thuế

```
python .claude/skills/tncn-personal-calc/scripts/personal_calc.py \
  --income <thu_nhap_nam> \
  --bhxh <bao_hiem_nam> \
  --dependents <so_npt> \
  --name "<ten_nguoi>" \
  --save
```

**Ví dụ:**
```
python .claude/skills/tncn-personal-calc/scripts/personal_calc.py --income 360000000 --bhxh 31500000 --dependents 1 --name "Nguyen Van A" --save
```

### Bước 3 — Đọc và trình bày kết quả

Đọc output terminal, trình bày cho người dùng gồm:
- Thuế TNCN phải nộp / năm
- Thuế suất hiệu dụng
- Thu nhập sau thuế (NET)
- Bảng phân tích theo 5 bậc (highlight bậc có thu nhập)

### Bước 4 — Thông báo file đã lưu

File kết quả được lưu tự động tại:
```
output/tncn_personal_{YYYY-MM-DD_HH-MM}.txt
```

---

## Lưu ý
- Thuế tính theo năm (biểu lũy tiến áp dụng cho thu nhập cả năm)
- Nếu người dùng hỏi về tháng cụ thể: nhân thu nhập tháng × 12 để ra năm, chia kết quả cho 12
- Bảo hiểm bắt buộc ≈ 10,5% lương đóng bảo hiểm (BHXH 8% + BHYT 1,5% + BHTN 1%)
