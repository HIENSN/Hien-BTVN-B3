# Claude Code Workspace — Quyết toán Thuế TNCN

Workspace cá nhân với 4 Claude Code skills hỗ trợ lập hồ sơ quyết toán thuế TNCN.
Áp dụng: **Luật Thuế TNCN số 109/2025/QH15** (hiệu lực 01/07/2026)

---

## Cấu trúc

```
.claude/
├── commands/
│   ├── tncn-generator.md
│   ├── tncn-sheets-sync.md
│   ├── tncn-review.md
│   └── tncn-full.md
└── skills/
    ├── tncn-generator/          # Skill 1
    │   ├── SKILL.md
    │   ├── scripts/
    │   │   └── generate_tncn.py
    │   └── templates/
    ├── tncn-sheets-sync/        # Skill 2
    │   ├── SKILL.md
    │   ├── config.json
    │   └── scripts/
    │       └── fetch_and_update.py
    ├── tncn-review/             # Skill 3
    │   ├── SKILL.md
    │   └── scripts/
    │       └── review_tncn.py
    └── tncn-full/               # Skill 4
        ├── SKILL.md
        └── scripts/
            └── run_all.py

05_QTT_TNCN_TT80_2025.xls       # Mẫu tờ khai chính thức (dùng cho Skill 1)

output/
    bang_luong_from_sheets.xlsx  # Skill 2 output: dữ liệu thô từ Google Sheets
    QuyetToanTNCN_2026.xls       # Skill 1 output: tờ khai quyết toán chính thức
    tncn_review_YYYY-MM-DD.xlsx  # Skill 3 output: báo cáo tổng hợp nhanh
    chat_history_*.txt           # Skill 1 output: lịch sử chạy
```

---

## 4 Skills

| Lệnh | Chức năng | Kết nối ngoài | File phụ |
|------|-----------|---------------|----------|
| `/tncn-sheets-sync` | Kết nối **Google Sheets** (public URL) → xuất file Excel thô | **Google Sheets** | `scripts/`, `config.json` |
| `/tncn-generator` | Đọc file Excel bảng lương → điền mẫu 05/QTT-TNCN chính thức | Không | `scripts/`, `templates/` |
| `/tncn-review` | Phân tích nhanh → báo cáo tổng hợp `.xlsx` | Không | `scripts/` |
| `/tncn-full` | **Chạy cả 3 skill trên theo thứ tự bằng 1 lệnh** | **Google Sheets** | `scripts/` |

---

## Flow sử dụng

```
Google Sheets  ──►  /tncn-sheets-sync  ──►  output/bang_luong_from_sheets.xlsx
                                                        │
                                    ┌───────────────────┴──────────────────┐
                                    ▼                                      ▼
                             /tncn-generator                         /tncn-review
                         QuyetToanTNCN_2026.xls              tncn_review_YYYY-MM-DD.xlsx
```

Mỗi khi dữ liệu Google Sheets thay đổi: chạy lại `/tncn-sheets-sync` → chạy `/tncn-generator` và/hoặc `/tncn-review` để có output cập nhật.

Hoặc dùng **`/tncn-full`** để chạy cả 3 bước chỉ bằng 1 lệnh.

---

## Yêu cầu Google Sheets (Skill 2)

Không cần API key hay credentials. Chỉ cần share Google Sheet với quyền **"Anyone with the link → Viewer"**.
Cập nhật `spreadsheet_id` và `gid` trong `.claude/skills/tncn-sheets-sync/config.json`.

---

## Quy định thuế áp dụng — Luật 109/2025/QH15

**Giảm trừ gia cảnh:**
- Bản thân: 15.500.000 VND/tháng
- Người phụ thuộc: 6.200.000 VND/người/tháng

**Biểu thuế lũy tiến 5 bậc:**

| Bậc | Thu nhập chịu thuế/tháng | Thuế suất |
|-----|--------------------------|-----------|
| 1 | Đến 10 triệu | 5% |
| 2 | Trên 10 – 30 triệu | 10% |
| 3 | Trên 30 – 60 triệu | 20% |
| 4 | Trên 60 – 100 triệu | 30% |
| 5 | Trên 100 triệu | 35% |
