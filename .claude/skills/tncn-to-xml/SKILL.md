---
name: tncn-to-xml
description: Chuyển đổi dữ liệu quyết toán TNCN sang định dạng XML chuẩn — đọc cùng file bảng lương với tncn-generator, xuất file XML có cấu trúc đầy đủ (tờ khai + phụ lục 01 + phụ lục 02)
---

## Mục đích
Từ file Excel bảng lương (cùng input với `/tncn-generator`), xuất file XML chuẩn
có thể dùng để lưu trữ, tích hợp hệ thống, hoặc nộp khai báo điện tử.

Output XML gồm đầy đủ:
- Thông tin chung (mẫu số, năm, căn cứ pháp lý)
- Tờ khai chính (tổng nhân sự, tổng TNCT, thuế)
- Phụ lục 01 — danh sách nhân viên có BHXH
- Phụ lục 02 — danh sách cộng tác viên không BHXH

---

## Các bước thực hiện

### Bước 1 — Nhận file đầu vào

**Nếu đã chạy `/tncn-sheets-sync` hoặc `/tncn-generator` trước đó**, mặc định dùng:
```
output/bang_luong_from_sheets.xlsx
```
Nếu không, yêu cầu người dùng cung cấp đường dẫn file Excel bảng lương.

### Bước 2 — Chạy script xuất XML

```
python .claude/skills/tncn-to-xml/scripts/to_xml.py "<duong_dan_file_bang_luong>"
```

**Ví dụ:**
```
python .claude/skills/tncn-to-xml/scripts/to_xml.py "output/bang_luong_from_sheets.xlsx"
```

### Bước 3 — Thông báo kết quả

File XML được lưu tại:
```
output/QuyetToanTNCN_{YYYY}.xml
```

Hiển thị cho người dùng:
- Số nhân viên PL01 / PL02
- Tổng thu nhập, tổng thuế
- Đường dẫn file XML đã lưu
- Snippet XML mẫu (10 dòng đầu)

---

## Flow kết hợp

```
Google Sheets
     │
     ▼
/tncn-sheets-sync  →  output/bang_luong_from_sheets.xlsx
                                    │
              ┌─────────────────────┼──────────────────────┐
              ▼                     ▼                      ▼
     /tncn-generator        /tncn-to-xml            /tncn-review
  QuyetToanTNCN.xls      QuyetToanTNCN.xml      tncn_review.xlsx
  (hồ sơ chính thức)     (khai báo điện tử)    (báo cáo nhanh)
```

---

## Lưu ý
- Dùng cùng logic aggregate với `tncn-generator` → số liệu luôn khớp nhau
- XML encoding UTF-8, có thể mở bằng bất kỳ text editor hoặc import vào hệ thống ERP
