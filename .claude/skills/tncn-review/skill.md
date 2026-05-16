---
name: tncn-review
description: Phân tích nhanh bảng lương và trả thông tin tổng quan thuế TNCN theo Luật 109/2025/QH15 ngay trong chat, không tạo file
---

## Mục đích
Xem nhanh tình hình thuế TNCN của toàn bộ nhân sự mà không cần tạo hồ sơ đầy đủ. Hữu ích để kiểm tra trước khi quyết toán hoặc phát hiện bất thường.

## Quy định áp dụng — Luật 109/2025/QH15
- Giảm trừ bản thân: 15.500.000 VND/tháng
- Giảm trừ người phụ thuộc: 6.200.000 VND/người/tháng
- Biểu thuế 5 bậc: 5% / 10% / 20% / 30% / 35%

## Bước 1 — Nhận dữ liệu
Người dùng cung cấp một trong hai cách:
- Đường dẫn file CSV → đọc bằng Bash: `cat "{đường_dẫn}"`
- Paste nội dung bảng trực tiếp vào chat

Nếu có 2 file (2 sheet), đọc và gộp cả hai.

## Bước 2 — Phân tích

**A. Tổng quan nhân sự**
- Tổng số nhân viên (unique theo Họ tên)
- Số người có BHXH (Phụ lục 01) vs không BHXH (Phụ lục 02)
- Kỳ dữ liệu: từ tháng nào đến tháng nào

**B. Chỉ số tài chính**
- Tổng thu nhập đã chi trả
- Tổng BHXH đã khấu trừ
- Tổng thuế TNCN đã khấu trừ tại nguồn
- Tổng thuế TNCN phải nộp theo Luật 109 (tính lại lũy tiến 5 bậc)
- Chênh lệch: còn phải nộp thêm hay được hoàn?

**C. Phân bổ theo bậc thuế (Luật 109)**
Số người rơi vào từng bậc dựa trên TNCT tháng trung bình:
- Không phải nộp (TNCT ≤ 0)
- Bậc 1 (TNCT ≤ 10 triệu/tháng)
- Bậc 2 (TNCT 10–30 triệu/tháng)
- Bậc 3 (TNCT 30–60 triệu/tháng)
- Bậc 4-5 (TNCT trên 60 triệu/tháng)

**D. Top & Bottom**
- Top 3 người đóng thuế nhiều nhất
- 3 người có thu nhập thấp nhất

**E. Cảnh báo bất thường**
- Nhân viên có chênh lệch lớn giữa thuế đã khấu trừ và thuế phải nộp theo Luật 109
- Dòng dữ liệu thiếu thông tin quan trọng

## Bước 3 — Trả kết quả trong chat
Trình bày theo bảng và gạch đầu dòng, không tạo file.

Cuối cùng gợi ý:
> "Để tạo bộ hồ sơ quyết toán đầy đủ: dùng `/tncn-generator` (từ file CSV) hoặc `/tncn-sheets-sync` (từ Google Sheets)."
