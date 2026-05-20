---
name: tncn-law-search
description: Tra cứu điều luật TNCN theo từ khóa — tìm kiếm trong 9 mục pháp lý của Luật 109/2025/QH15, hiển thị nội dung liên quan
---

## Mục đích
Tra cứu nhanh các điều khoản, quy định, mức giảm trừ, biểu thuế trong Luật Thuế TNCN 2026.
Port trực tiếp từ nội dung `DEFAULT_SECTIONS` trong `luat.html` của Mini Tool TNCN.

## 9 Mục luật có sẵn

| # | Tiêu đề | Từ khóa gợi ý |
|---|---|---|
| 1 | Cơ sở pháp lý | luật, 109, văn bản, căn cứ |
| 2 | Đối tượng nộp thuế | cư trú, 183 ngày, ai phải nộp |
| 3 | Thu nhập chịu thuế | lương, lãi, cổ tức, kinh doanh |
| 4 | Giảm trừ gia cảnh | 15.5 triệu, BHXH, người phụ thuộc |
| 5 | Biểu thuế lũy tiến 5 bậc | 5%, 10%, 20%, bậc thuế |
| 6 | Cách tính thuế | công thức, ví dụ, hướng dẫn |
| 7 | Người phụ thuộc | con, vợ chồng, cha mẹ |
| 8 | Thu nhập miễn thuế | lãi tiết kiệm, kiều hối, làm thêm giờ |
| 9 | Quyết toán thuế TNCN | thời hạn, tháng 3, tháng 4, hoàn thuế |

---

## Các bước thực hiện

### Bước 1 — Nhận từ khóa từ người dùng

Xác định từ khóa người dùng muốn tra cứu từ câu hỏi của họ.

**Ví dụ câu hỏi → từ khóa:**
- "Lãi tiền gửi có chịu thuế không?" → từ khóa: `miễn thuế`
- "Mức giảm trừ người phụ thuộc là bao nhiêu?" → từ khóa: `giảm trừ`
- "Hạn nộp quyết toán khi nào?" → từ khóa: `quyết toán`

### Bước 2 — Chạy script tra cứu

```
python .claude/skills/tncn-law-search/scripts/law_search.py "<tu_khoa>"
```

**Các tùy chọn:**
```
# Tìm theo từ khóa
python .claude/skills/tncn-law-search/scripts/law_search.py "giảm trừ"

# Xem toàn bộ nội dung khi tìm thấy nhiều mục
python .claude/skills/tncn-law-search/scripts/law_search.py "thuế" --all

# Liệt kê danh sách 9 mục (không nội dung)
python .claude/skills/tncn-law-search/scripts/law_search.py --list
```

### Bước 3 — Trình bày kết quả cho người dùng

Đọc output terminal và trả lời câu hỏi của người dùng dựa trên nội dung tìm được.
Trích dẫn mục luật liên quan, giải thích ngắn gọn theo ngữ cảnh câu hỏi.

---

## Kết hợp với skill khác

```
/tncn-law-search  →  Tra cứu quy định  →  Giải đáp thắc mắc cụ thể
                                                    │
                                                    ▼
                                         /tncn-personal-calc
                                       Tính thuế thực tế cho người dùng
```
