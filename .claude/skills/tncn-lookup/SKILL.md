---
name: tncn-lookup
description: Tra cứu thông tin nhân sự từ Google Sheets và liên kết với Mini Tool tính thuế TNCN — tìm theo họ tên, tự động điền thu nhập và BHXH vào công cụ tính thuế
---

## Mục đích
Kết nối Mini Tool tính thuế TNCN với dữ liệu bảng lương thực tế trên Google Sheets.
Khi nhân viên nhập đúng họ tên, Mini Tool tự động điền:
- Tổng thu nhập / năm (cộng dồn tất cả các kỳ lương)
- BHXH đã khấu trừ / năm

## Google Sheets nguồn dữ liệu

| Thông tin | Giá trị |
|---|---|
| Spreadsheet ID | `1Ux1aaL2q9A73HTKpBQEOoari5F5tltI5J8-j65mlCmM` |
| Sheet chính | `Tổng thu nhập` (gid=0) — nhân viên có BHXH |
| Sheet phụ | `CTV` (gid=1758432323) — cộng tác viên |
| Điều kiện | Sheet phải share "Anyone with the link → Viewer" |

## Mini Tool (đã tích hợp)

**File:** `D:\Học Claude code\Mini Tool Tinh thue TNCN\index.html`
**Deploy:** https://hiensn.github.io/mini-tool-tncn-2026/

Tính năng đã thêm vào index.html:
- Trường **Họ và tên** — dùng để tra cứu bảng lương
- Trường **Số CCCD / CMND** — thông tin tham khảo (lưu nhận dạng)
- Nút **"Tra cứu từ bảng lương"** — fetch CSV từ Google Sheets, tìm theo tên, auto-fill

## Cách hoạt động (trong trình duyệt)

```
Người dùng nhập "Họ và tên"
        │
        ▼
fetch CSV từ Google Sheets (public, không cần API key)
        │
        ▼
Tìm tất cả dòng khớp tên (case-insensitive, bỏ dấu)
        │
        ▼
Tổng hợp: sum(Tổng thu nhập) + sum(BHXH khấu trừ)
        │
        ▼
Auto-fill ô thu nhập + BHXH trong form tính thuế
        │
        ▼
Người dùng điền thêm Số người phụ thuộc → nhấn Tính thuế
```

## Lưu ý quan trọng

- **Chỉ hoạt động trên GitHub Pages** — tính năng fetch bị chặn khi mở file `index.html` trực tiếp (`file://` protocol)
- Tra cứu theo **tên** (không phải CCCD vì sheet chưa có cột CCCD)
- Tên phải nhập **đúng chính tả** (đã xử lý bỏ dấu và uppercase để so khớp linh hoạt)
- Số người phụ thuộc vẫn phải nhập tay (không có trong sheet)

## Hướng dẫn sử dụng (cho người dùng cuối)

1. Mở https://hiensn.github.io/mini-tool-tncn-2026/
2. Nhập **Họ và tên** vào ô "Thông tin nhân sự"
3. Nhấn **"Tra cứu từ bảng lương"**
4. Hệ thống tự điền thu nhập và BHXH
5. Nhập thêm **Số người phụ thuộc** (nếu có)
6. Nhấn **"Tính thuế TNCN"**

## Khi được hỏi về skill này

Giải thích flow trên và hướng dẫn người dùng mở đúng URL GitHub Pages.
Nếu người dùng báo lỗi "không tra cứu được": kiểm tra họ đang mở bằng `file://` hay GitHub Pages.
