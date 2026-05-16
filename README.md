# Claude Code Workspace — Quyết toán Thuế TNCN

Workspace cá nhân với 3 Claude Code skills hỗ trợ lập hồ sơ quyết toán thuế TNCN.
Áp dụng: **Luật Thuế TNCN số 109/2025/QH15** (hiệu lực 01/07/2026)

## Cấu trúc

```
.claude/skills/
├── tncn-generator/          # Skill 1: Tạo hồ sơ từ file CSV
│   ├── skill.md
│   └── templates/           # 4 mẫu biểu theo TT 80/2021
│       ├── to_khai_chinh.txt
│       ├── phu_luc_01.txt
│       ├── phu_luc_02.txt
│       └── phu_luc_03.txt
│
├── tncn-sheets-sync/        # Skill 2: Đồng bộ từ Google Sheets API
│   ├── skill.md
│   ├── config.json
│   └── scripts/
│       └── fetch_and_update.py
│
└── tncn-review/             # Skill 3: Review nhanh, tổng quan
    └── skill.md

output/                      # File kết quả (tạo tự động khi chạy skill)
```

## 3 Skills

| Lệnh | Chức năng | API ngoài | File phụ |
|------|-----------|-----------|----------|
| `/tncn-generator` | Đọc CSV → tạo đầy đủ hồ sơ quyết toán | Không | `templates/` |
| `/tncn-sheets-sync` | Kết nối Google Sheets → đồng bộ hồ sơ | **Google Sheets API** | `config.json`, `scripts/` |
| `/tncn-review` | Phân tích nhanh, tổng quan thuế | Không | Không |

## Quy định thuế áp dụng (Luật 109/2025/QH15)

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

## Đầu ra (thư mục output/)

| File | Tạo bởi | Mô tả |
|------|---------|-------|
| `05_QTT-TNCN_{YYYY}.txt` | Skill 1, 2 | Tờ khai quyết toán chính |
| `05-1_BK-QTT-TNCN_{YYYY}.txt` | Skill 1, 2 | Phụ lục 01 — có BHXH |
| `05-2_BK-QTT-TNCN_{YYYY}.txt` | Skill 1, 2 | Phụ lục 02 — không BHXH |
| `05-3_BK-QTT-TNCN_{YYYY}.txt` | Skill 1, 2 | Phụ lục 03 — người phụ thuộc |
| `chat_history_{YYYY-MM-DD}.txt` | Skill 1, 2 | Lịch sử chat và tóm tắt kết quả |

## Cài đặt Google Sheets API (cho Skill 2)

1. Vào [Google Cloud Console](https://console.cloud.google.com) → Tạo project
2. Enable **Google Sheets API**
3. Tạo **Service Account** → tải file key JSON → đổi tên thành `credentials.json`
4. Đặt vào `.claude/skills/tncn-sheets-sync/`
5. Chia sẻ Google Sheet với email service account (quyền Viewer)
6. Điền `spreadsheet_id` và `sheet1_gid` vào `config.json`
