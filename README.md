# Claude Code Workspace — Quyết toán Thuế TNCN

Workspace Claude Code với **8 skills** và **2 agents** hỗ trợ toàn bộ quy trình thuế TNCN:
từ đồng bộ dữ liệu bảng lương → lập hồ sơ quyết toán → khai báo điện tử → tư vấn cá nhân.

**Luật áp dụng:** Luật Thuế TNCN số 109/2025/QH15 (hiệu lực 01/01/2026)

---

## Cấu trúc thư mục

```
.claude/
├── agents/
│   ├── bao-cao-thue.md          # Agent 1: Báo cáo thuế doanh nghiệp
│   └── tu-van-ca-nhan.md        # Agent 2: Tư vấn thuế cá nhân
├── commands/                    # Slash commands kích hoạt từng skill
│   ├── tncn-sheets-sync.md
│   ├── tncn-generator.md
│   ├── tncn-review.md
│   ├── tncn-full.md
│   ├── tncn-personal-calc.md
│   ├── tncn-law-search.md
│   ├── tncn-to-xml.md
│   └── tncn-lookup.md
└── skills/
    ├── tncn-sheets-sync/        # Skill 1: Đồng bộ Google Sheets
    ├── tncn-generator/          # Skill 2: Tạo hồ sơ 05/QTT-TNCN
    ├── tncn-review/             # Skill 3: Báo cáo tổng hợp nhanh
    ├── tncn-full/               # Skill 4: Chạy toàn bộ pipeline
    ├── tncn-personal-calc/      # Skill 5: Tính thuế 1 cá nhân
    ├── tncn-law-search/         # Skill 6: Tra cứu điều luật
    ├── tncn-to-xml/             # Skill 7: Xuất XML khai báo điện tử
    └── tncn-lookup/             # Skill 8: Liên kết Mini Tool ↔ Google Sheets

05_QTT_TNCN_TT80_2025.xls       # Mẫu tờ khai chính thức

output/
    bang_luong_from_sheets.xlsx                  # Dữ liệu thô từ Google Sheets
    QuyetToanTNCN_2026.xls                       # Hồ sơ 05/QTT-TNCN chính thức
    QuyetToanTNCN_2026.xml                       # File XML khai báo điện tử
    tncn_review_YYYY-MM-DD.xlsx                  # Báo cáo tổng hợp nhanh
    tncn_personal_YYYY-MM-DD_HH-MM.txt           # Kết quả tính thuế cá nhân
    agent_bao_cao_thue_YYYY-MM.txt               # Output từ Agent báo cáo thuế
    agent_tu_van_ca_nhan_<TenNhanVien>.txt        # Output từ Agent tư vấn
    chat_history_*.txt                           # Lịch sử chạy
```

---

## 2 Agents

### Agent 1 — `bao-cao-thue` (Báo cáo thuế doanh nghiệp)

**Mục đích:** Lập bộ hồ sơ quyết toán thuế TNCN hàng tháng đầy đủ, sẵn sàng nộp cơ quan thuế.

**Skills sử dụng:** `tncn-full` + `tncn-to-xml`

**Nguyên tắc:**
- Báo cáo lập **mỗi tháng một lần**
- Số liệu từ ngày 1 đến ngày cuối tháng
- Output: `QuyetToanTNCN.xls` (hồ sơ chính thức) + `QuyetToanTNCN.xml` (khai báo điện tử)

### Agent 2 — `tu-van-ca-nhan` (Tư vấn thuế cá nhân)

**Mục đích:** Hỗ trợ người lao động tự tra cứu và tính thuế TNCN của mình.

**Skills sử dụng:** `tncn-personal-calc` + `tncn-law-search` + `tncn-lookup`

**Nguyên tắc:**
- Người lao động tra cứu **bất cứ lúc nào**
- Số liệu cập nhật theo thời gian thực từ Google Sheets
- Hỗ trợ 3 nhu cầu: tra cứu bảng lương → tính thuế → giải đáp pháp luật

---

## 8 Skills

| Lệnh | Chức năng | Input | Output |
|------|-----------|-------|--------|
| `/tncn-sheets-sync` | Đồng bộ dữ liệu từ Google Sheets | Google Sheets (public) | `bang_luong_from_sheets.xlsx` |
| `/tncn-generator` | Tạo hồ sơ quyết toán 05/QTT-TNCN | File Excel bảng lương | `QuyetToanTNCN_{YYYY}.xls` |
| `/tncn-review` | Báo cáo tổng hợp nhanh | File Excel bảng lương | `tncn_review_{date}.xlsx` |
| `/tncn-full` | Chạy cả 3 skill trên bằng 1 lệnh | Google Sheets | XLS + XLSX + chat history |
| `/tncn-personal-calc` | Tính thuế TNCN cho 1 cá nhân | Thu nhập, BHXH, NPT | Kết quả thuế + file TXT |
| `/tncn-law-search` | Tra cứu 9 mục điều luật TNCN | Từ khóa | Nội dung luật liên quan |
| `/tncn-to-xml` | Chuyển đổi quyết toán sang XML | File Excel bảng lương | `QuyetToanTNCN_{YYYY}.xml` |
| `/tncn-lookup` | Liên kết Mini Tool với Google Sheets | Họ tên nhân viên | Auto-fill thu nhập + BHXH |

---

## Flow tổng thể

```
Google Sheets (bảng lương thực tế)
        │
        ▼
/tncn-sheets-sync  →  output/bang_luong_from_sheets.xlsx
        │
        ├──────────────────┬──────────────────┬──────────────────┐
        ▼                  ▼                  ▼                  ▼
/tncn-generator    /tncn-review        /tncn-to-xml       /tncn-lookup
QuyetToan.xls    tncn_review.xlsx    QuyetToan.xml     (Mini Tool web)
(hồ sơ PL01/02)  (báo cáo nhanh)   (khai báo điện tử)

                               ↑ tncn-full chạy 3 bước đầu cùng lúc ↑

/tncn-personal-calc  →  tính thuế 1 người, xuất TXT
/tncn-law-search     →  tra cứu luật theo từ khóa
```

---

## Mini Tool tích hợp

**Web app tính thuế TNCN:** https://hiensn.github.io/mini-tool-tncn-2026/

Tính năng `/tncn-lookup` đã được tích hợp vào Mini Tool:
- Nhập **Họ và tên** → tra cứu bảng lương từ Google Sheets
- Tự động điền thu nhập và BHXH vào form tính thuế
- Yêu cầu: mở qua GitHub Pages (không dùng được khi mở file:// trực tiếp)

---

## Quy định thuế áp dụng — Luật 109/2025/QH15

**Giảm trừ gia cảnh:**

| Khoản | Tháng | Năm |
|-------|-------|-----|
| Bản thân người nộp thuế | 15.500.000 đ | 186.000.000 đ |
| Mỗi người phụ thuộc | 6.200.000 đ | 74.400.000 đ |

**Biểu thuế lũy tiến 5 bậc:**

| Bậc | Thu nhập tính thuế / năm | Thuế suất |
|-----|--------------------------|-----------|
| 1 | Đến 120 triệu | 5% |
| 2 | Trên 120 – 360 triệu | 10% |
| 3 | Trên 360 – 720 triệu | 20% |
| 4 | Trên 720 – 1.200 triệu | 30% |
| 5 | Trên 1.200 triệu | 35% |

---

## Yêu cầu môi trường

```bash
pip install openpyxl xlrd xlutils xlwt
```

Google Sheets cần share: **"Anyone with the link → Viewer"** (không cần API key).

---

## Liên kết

- **Repo này (Skill workspace):** https://github.com/HIENSN/Hien-BTVN-B3
- **Mini Tool web:** https://github.com/HIENSN/mini-tool-tncn-2026
- **Mini Tool deploy:** https://hiensn.github.io/mini-tool-tncn-2026/
- **Google Sheets bảng lương:** https://docs.google.com/spreadsheets/d/1Ux1aaL2q9A73HTKpBQEOoari5F5tltI5J8-j65mlCmM
