#!/usr/bin/env python3
"""
Tra cuu dieu luat TNCN theo tu khoa
Port tu noi dung DEFAULT_SECTIONS trong luat.html cua Mini Tool TNCN
"""

import argparse
import sys

LAW_SECTIONS = [
    {
        "id": "s1",
        "title": "Co so phap ly",
        "keywords": ["phap ly", "luat", "109", "2025", "nghi quyet", "110",
                     "can cu", "van ban", "thong tu", "nghi dinh", "co so"],
        "content": """Cac van ban phap luat ap dung cho viec tinh thue TNCN tu 01/01/2026:

  * Luat Thue TNCN so 109/2025/QH15 ban hanh ngay 25/11/2025
    -- Quy dinh bieu thue luy tien tung phan moi gom 5 bac.
  * Nghi quyet so 110/2025/UBTVQH15
    -- Dieu chinh muc giam tru gia canh.
  * Nghi dinh huong dan cua Chinh phu va Thong tu cua Bo Tai chinh.

  Luu y: Luat moi thay the Luat Thue TNCN nam 2007 (sua doi 2012, 2014)
  va cac van ban huong dan truoc day.""",
    },
    {
        "id": "s2",
        "title": "Doi tuong nop thue",
        "keywords": ["doi tuong", "cu tru", "khong cu tru", "183 ngay",
                     "thuong tru", "nguoi nop thue", "ai", "phai nop"],
        "content": """Doi tuong nop thue TNCN bao gom:

  1. Ca nhan cu tru  -- co thu nhap chiu thue phat sinh trong VA ngoai VN.
  2. Ca nhan khong cu tru -- co thu nhap chiu thue phat sinh TRONG lanh tho VN.

  Ca nhan cu tru la nguoi dap ung MOT trong cac dieu kien:
  * Co mat tai Viet Nam tu 183 ngay tro len trong mot nam duong lich
    hoac 12 thang lien tuc.
  * Co noi o thuong xuyen tai Viet Nam (dang ky thuong tru hoac
    nha thue >= 183 ngay/nam).""",
    },
    {
        "id": "s3",
        "title": "Thu nhap chiu thue",
        "keywords": ["thu nhap", "chiu thue", "luong", "lai", "co tuc",
                     "bat dong san", "trung thuong", "ban quyen", "thua ke",
                     "qua tang", "kinh doanh", "dau tu", "chuyen nhuong"],
        "content": """Thu nhap chiu thue TNCN gom 10 loai chinh:

   1. Thu nhap tu kinh doanh
   2. Thu nhap tu tien luong, tien cong
   3. Thu nhap tu dau tu von (lai cho vay, loi tuc co phan...)
   4. Thu nhap tu chuyen nhuong von
   5. Thu nhap tu chuyen nhuong bat dong san
   6. Thu nhap tu trung thuong
   7. Thu nhap tu ban quyen
   8. Thu nhap tu nhuong quyen thuong mai
   9. Thu nhap tu nhan thua ke (chung khoan, von, BDS...)
  10. Thu nhap tu nhan qua tang (chung khoan, von, BDS...)""",
    },
    {
        "id": "s4",
        "title": "Giam tru gia canh",
        "keywords": ["giam tru", "gia canh", "ban than", "nguoi phu thuoc",
                     "15.5", "6.2", "186", "74.4", "bhxh", "bhyt",
                     "bao hiem", "huu tri", "tu thien", "muc giam tru"],
        "content": """Theo Nghi quyet 110/2025/UBTVQH15, tu ky tinh thue 2026:

  +--------------------------------------------+-----------------+-----------------+
  | Khoan giam tru                             | Muc / thang     | Muc / nam       |
  +--------------------------------------------+-----------------+-----------------+
  | Giam tru cho ban than nguoi nop thue       | 15.500.000 d    | 186.000.000 d   |
  | Giam tru cho moi nguoi phu thuoc           |  6.200.000 d    |  74.400.000 d   |
  +--------------------------------------------+-----------------+-----------------+

  Ngoai ra con duoc tru them:
  * Bao hiem bat buoc: BHXH (8%) + BHYT (1,5%) + BHTN (1%) = 10,5% luong dong BH.
  * Quy huu tri tu nguyen (toi da 1 trieu dong/thang).
  * Dong gop tu thien, nhan dao, khuyen hoc (co chung tu hop le).""",
    },
    {
        "id": "s5",
        "title": "Bieu thue luy tien tung phan (5 bac)",
        "keywords": ["bieu thue", "luy tien", "5 bac", "5%", "10%", "20%",
                     "30%", "35%", "thue suat", "bac 1", "bac 2", "bac 3",
                     "bac 4", "bac 5", "120 trieu", "360", "720", "1200"],
        "content": """Ap dung cho thu nhap tu tien luong, tien cong cua ca nhan cu tru:

  +------+------------------------------+------------------------+-----------+
  | Bac  | Thu nhap tinh thue / NAM     | Thu nhap tinh thue / th| Thue suat |
  +------+------------------------------+------------------------+-----------+
  |  1   | Den 120 trieu                | Den 10 trieu           |    5%     |
  |  2   | Tren 120 -- 360 trieu        | Tren 10 -- 30 trieu    |   10%     |
  |  3   | Tren 360 -- 720 trieu        | Tren 30 -- 60 trieu    |   20%     |
  |  4   | Tren 720 -- 1.200 trieu      | Tren 60 -- 100 trieu   |   30%     |
  |  5   | Tren 1.200 trieu             | Tren 100 trieu         |   35%     |
  +------+------------------------------+------------------------+-----------+

  So voi bieu thue cu (7 bac): bieu moi gon hon, gian khoang cach cac bac,
  giam ganh nang cho nguoi thu nhap trung binh.""",
    },
    {
        "id": "s6",
        "title": "Cach tinh thue",
        "keywords": ["cach tinh", "cong thuc", "vi du", "tinh nhu the nao",
                     "minh hoa", "thu nhap tinh thue", "huong dan tinh"],
        "content": """Cong thuc tong quat:

  Thue TNCN = Thu nhap tinh thue x Thue suat (luy tien)
  Thu nhap tinh thue = Tong thu nhap - BH bat buoc - Giam tru gia canh - Mien thue

  Vi du minh hoa:
  Anh A thu nhap 30 trieu/thang (360 trieu/nam), 1 nguoi phu thuoc,
  dong BHXH 31,5 trieu/nam:

    Giam tru ban than              : 186.000.000 d
    Giam tru 1 nguoi phu thuoc     :  74.400.000 d
    Bao hiem bat buoc              :  31.500.000 d
    ---------------------------------------------------
    Thu nhap tinh thue = 360.000.000 - 186.000.000 - 74.400.000 - 31.500.000
                       = 68.100.000 d
    Thue phai nop (Bac 1, 5%)      = 68.100.000 x 5% = 3.405.000 d/nam""",
    },
    {
        "id": "s7",
        "title": "Nguoi phu thuoc",
        "keywords": ["nguoi phu thuoc", "npt", "con", "vo", "chong",
                     "cha me", "nuoi duong", "khuyet tat", "dai hoc",
                     "18 tuoi", "ong ba", "dieu kien"],
        "content": """Nguoi phu thuoc la nguoi ma nguoi nop thue co nghia vu nuoi duong:

  * Con: con duoi 18 tuoi; hoac con tu 18 tuoi bi khuyet tat/khong co kha nang
    lao dong; hoac con dang hoc DH/CD/THCN/day nghe va thu nhap <= 1 trieu/thang.
  * Vo/chong: khong co kha nang lao dong hoac thu nhap <= 1 trieu dong/thang.
  * Cha me de, cha me vo/chong, cha me nuoi hop phap: ngoai tuoi lao dong
    hoac bi khuyet tat/khong co kha nang lao dong.
  * Nguoi khac phai truc tiep nuoi duong (anh chi em ruot, ong ba,
    co di chu bac ruot, chau ruot, nguoi theo phap luat).

  Luu y: Moi nguoi phu thuoc chi duoc tinh giam tru MOT LAN
  cho mot nguoi nop thue trong nam tinh thue.""",
    },
    {
        "id": "s8",
        "title": "Cac khoan thu nhap duoc mien thue",
        "keywords": ["mien thue", "lai tiet kiem", "lai tien gui", "kieu hoi",
                     "lam them gio", "luong huu", "hoc bong", "boi thuong",
                     "nha o duy nhat", "khong phai nop thue", "duoc tru"],
        "content": """Cac khoan thu nhap duoc mien thue TNCN:

  * Chuyen nhuong BDS giua vo-chong, cha me-con, ong ba-chau, anh chi em ruot.
  * Chuyen nhuong nha o duy nhat (so huu >= 6 thang).
  * Lai tien gui tai ngan hang, to chuc tin dung; lai trai phieu Chinh phu.
  * Thu nhap tu kieu hoi.
  * Phan tien luong lam viec ban dem, lam them gio duoc tra cao hon so chuan.
  * Tien luong huu do Quy BHXH chi tra; luong huu quy huu tri tu nguyen.
  * Hoc bong nhan tu ngan sach nha nuoc hoac to chuc trong/ngoai nuoc.
  * Tien boi thuong bao hiem, tai nan lao dong, tro cap sinh con, nuon con nuoi...""",
    },
    {
        "id": "s9",
        "title": "Quyet toan thue TNCN",
        "keywords": ["quyet toan", "hoan thue", "nop them", "thoi han",
                     "thang 3", "thang 4", "uy quyen", "to chuc tra thu nhap",
                     "05/qtt", "finalize", "deadline", "han nop"],
        "content": """Ca nhan co nghia vu quyet toan thue TNCN neu:
  * Co so thue phai nop them so voi so da tam nop.
  * Co yeu cau hoan thue hoac bu tru vao ky tiep theo.

  Thoi han quyet toan:
  * Ca nhan tu quyet toan   : cham nhat cuoi THANG 4 nam sau.
  * To chuc quyet toan thay : cham nhat cuoi THANG 3 nam sau.

  Luu y: Ca nhan co the uy quyen cho to chuc tra thu nhap quyet toan thay
  neu chi co MOT nguon thu nhap tu tien luong, tien cong.""",
    },
]


def search(keyword):
    if not keyword or not keyword.strip():
        return LAW_SECTIONS

    q = keyword.strip().lower()
    # Loai bo dau tieng Viet don gian (khong dung unidecode)
    results = []
    for sec in LAW_SECTIONS:
        title_hit   = q in sec["title"].lower()
        content_hit = q in sec["content"].lower()
        kw_hit      = any(q in kw.lower() for kw in sec["keywords"])
        if title_hit or content_hit or kw_hit:
            results.append(sec)
    return results


def print_section(sec, idx, full=True):
    width = 60
    title_line = f"  Muc {idx}: {sec['title']}"
    print()
    print(title_line)
    print("  " + "-" * (width - 2))
    if full:
        for line in sec["content"].split("\n"):
            print(f"  {line}")
    else:
        lines = [l for l in sec["content"].split("\n") if l.strip()][:4]
        for line in lines:
            print(f"  {line}")
        print("  ...")
    print()


def main():
    parser = argparse.ArgumentParser(description="Tra cuu luat TNCN 2026 theo tu khoa")
    parser.add_argument("keyword", nargs="?", default="",
                        help="Tu khoa tim kiem (bo trong de hien thi tat ca)")
    parser.add_argument("--all",  action="store_true",
                        help="Hien thi toan bo noi dung khi tim thay nhieu muc")
    parser.add_argument("--list", action="store_true",
                        help="Chi liet ke ten 9 muc, khong hien thi noi dung")
    args = parser.parse_args()

    print()
    print("=" * 60)
    print("  TRA CUU LUAT THUE TNCN 2026")
    print("  Luat so 109/2025/QH15 -- ap dung tu 01/01/2026")
    print("=" * 60)

    if args.list:
        print()
        print("  Danh sach 9 muc luat:")
        for i, sec in enumerate(LAW_SECTIONS, 1):
            print(f"  {i:2}. {sec['title']}")
        print()
        return

    results = search(args.keyword)

    if args.keyword:
        print(f'\n  Tim kiem: "{args.keyword}"')
        print(f"  Ket qua : {len(results)}/{len(LAW_SECTIONS)} muc phu hop")
    else:
        print(f"\n  Hien thi toan bo {len(LAW_SECTIONS)} muc luat")

    if not results:
        print()
        print("  Khong tim thay muc nao phu hop.")
        print("  Goi y tu khoa: bieu thue | giam tru | mien thue | quyet toan | nguoi phu thuoc")
        print()
        return

    show_full = args.all or len(results) <= 2
    for i, sec in enumerate(results, 1):
        print_section(sec, i, full=show_full)

    if len(results) > 2 and not args.all:
        print(f"  Tim thay {len(results)} muc. Them --all de xem day du noi dung.")

    print()
    print("  Xem truc tuyen: https://hiensn.github.io/mini-tool-tncn-2026/luat.html")
    print()


if __name__ == "__main__":
    main()
