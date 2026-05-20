#!/usr/bin/env python3
"""
Tinh thue TNCN ca nhan theo Luat 109/2025/QH15
Port tu logic JavaScript index.html cua Mini Tool TNCN
"""

import argparse
import os
from datetime import datetime

PERSONAL_DEDUCTION  = 186_000_000   # 186tr/nam = 15.5tr/thang
DEPENDENT_DEDUCTION =  74_400_000   # 74.4tr/nam = 6.2tr/thang

BRACKETS = [
    {"up_to": 120_000_000,      "rate": 0.05, "label": "Den 120 trieu"},
    {"up_to": 360_000_000,      "rate": 0.10, "label": "120 - 360 trieu"},
    {"up_to": 720_000_000,      "rate": 0.20, "label": "360 - 720 trieu"},
    {"up_to": 1_200_000_000,    "rate": 0.30, "label": "720 - 1.200 trieu"},
    {"up_to": float("inf"),     "rate": 0.35, "label": "Tren 1.200 trieu"},
]


def fmt(n):
    return f"{int(round(n)):,}".replace(",", ".") + " d"


def calc_tax(income, bhxh, dependents):
    family_deduction = PERSONAL_DEDUCTION + dependents * DEPENDENT_DEDUCTION
    taxable_income = max(0, income - bhxh - family_deduction)

    remaining = taxable_income
    prev_cap = 0
    total_tax = 0
    breakdown = []

    for b in BRACKETS:
        cap = b["up_to"]
        if cap == float("inf"):
            slice_amt = remaining
        else:
            slice_amt = max(0, min(remaining, cap - prev_cap))

        tax = slice_amt * b["rate"]
        breakdown.append({
            "label": b["label"],
            "rate":  b["rate"],
            "slice": slice_amt,
            "tax":   tax,
            "active": slice_amt > 0,
        })
        total_tax += tax
        remaining -= slice_amt
        if cap != float("inf"):
            prev_cap = cap

    eff_rate   = (total_tax / income * 100) if income > 0 else 0
    net_income = income - bhxh - total_tax

    return {
        "income":          income,
        "bhxh":            bhxh,
        "dependents":      dependents,
        "family_deduction": family_deduction,
        "taxable_income":  taxable_income,
        "total_tax":       total_tax,
        "eff_rate":        eff_rate,
        "net_income":      net_income,
        "breakdown":       breakdown,
    }


def print_result(result, name=""):
    sep = "-" * 60
    title = f"KET QUA TINH THUE TNCN{' -- ' + name.upper() if name else ''}"
    print()
    print("=" * 60)
    print(f"  {title}")
    print("  Luat so 109/2025/QH15 -- ap dung tu 01/01/2026")
    print("=" * 60)
    print()
    print(f"  Tong thu nhap chiu thue   : {fmt(result['income'])}")
    print(f"  - Bao hiem bat buoc        : {fmt(result['bhxh'])}")
    print(f"  - Giam tru ban than        : {fmt(PERSONAL_DEDUCTION)}")
    print(f"  - Giam tru {result['dependents']} NPT x {fmt(DEPENDENT_DEDUCTION)}: {fmt(result['dependents'] * DEPENDENT_DEDUCTION)}")
    print(sep)
    print(f"  Thu nhap tinh thue         : {fmt(result['taxable_income'])}")
    print()
    print(f"  *** THUE TNCN PHAI NOP    : {fmt(result['total_tax'])} ***")
    print(f"  Thue suat hieu dung        : {result['eff_rate']:.2f}%")
    print(f"  Thu nhap sau thue (NET)    : {fmt(result['net_income'])}")
    print()
    print(sep)
    print("  PHAN TICH THEO BAC THUE:")
    print(sep)
    header = f"  {'Bac':<6} {'Khoang (nam)':<24} {'Thue suat':<12} {'Phan TN':<22} {'So thue'}"
    print(header)
    print(sep)
    for i, b in enumerate(result["breakdown"], 1):
        mark = ">" if b["active"] else " "
        slice_str = fmt(b["slice"]) if b["slice"] > 0 else "---"
        tax_str   = fmt(b["tax"])   if b["tax"]   > 0 else "---"
        rate_str  = f"{int(b['rate']*100)}%"
        print(f"  {mark}{i:<5} {b['label']:<24} {rate_str:<12} {slice_str:<22} {tax_str}")
    print("=" * 60)
    print()


def save_result(result, name=""):
    os.makedirs("output", exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M")
    path = f"output/tncn_personal_{ts}.txt"

    lines = [
        "KET QUA TINH THUE TNCN CA NHAN 2026",
        f"Luat so 109/2025/QH15 -- {datetime.now().strftime('%d/%m/%Y %H:%M')}",
    ]
    if name:
        lines.append(f"Nguoi nop thue: {name}")
    lines += [
        "",
        f"Tong thu nhap chiu thue : {fmt(result['income'])}",
        f"Bao hiem bat buoc       : {fmt(result['bhxh'])}",
        f"Giam tru gia canh       : {fmt(result['family_deduction'])}",
        f"  (Ban than {fmt(PERSONAL_DEDUCTION)} + {result['dependents']} NTP x {fmt(DEPENDENT_DEDUCTION)})",
        f"Thu nhap tinh thue      : {fmt(result['taxable_income'])}",
        f"THUE TNCN PHAI NOP      : {fmt(result['total_tax'])}",
        f"Thue suat hieu dung     : {result['eff_rate']:.2f}%",
        f"Thu nhap sau thue (NET) : {fmt(result['net_income'])}",
        "",
        "PHAN TICH THEO BAC:",
    ]
    for i, b in enumerate(result["breakdown"], 1):
        if b["active"]:
            lines.append(
                f"  Bac {i} ({int(b['rate']*100)}%) -- {b['label']}: "
                f"TN = {fmt(b['slice'])}, Thue = {fmt(b['tax'])}"
            )

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return path


def main():
    parser = argparse.ArgumentParser(description="Tinh thue TNCN ca nhan 2026")
    parser.add_argument("--income",     type=float, required=True, help="Tong thu nhap chiu thue/nam (VND)")
    parser.add_argument("--bhxh",       type=float, default=0,     help="Bao hiem bat buoc da dong/nam (VND)")
    parser.add_argument("--dependents", type=int,   default=0,     help="So nguoi phu thuoc")
    parser.add_argument("--name",       type=str,   default="",    help="Ten nguoi tinh thue")
    parser.add_argument("--save",       action="store_true",       help="Luu ket qua ra file")
    args = parser.parse_args()

    result = calc_tax(args.income, args.bhxh, args.dependents)
    print_result(result, args.name)

    if args.save:
        path = save_result(result, args.name)
        print(f"  Da luu ket qua: {path}")
        print()


if __name__ == "__main__":
    main()
