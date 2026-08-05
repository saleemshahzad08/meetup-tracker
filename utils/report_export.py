"""
utils/report_export.py — builds a Markdown summary of payments and
expenses. Deliberately text-only: no receipt images are included.

Uses only Python's standard library (no reportlab, no third-party
packages), specifically so this can never fail to compile as part of
the Android build - it's plain string formatting, nothing more.
"""

import os
from datetime import datetime


def generate_markdown_report(payments, expenses, totals, output_path):
    """
    payments: list of dicts with keys name, amount, timestamp
    expenses: list of dicts with keys item, amount, timestamp
    totals: dict with keys collected, spent, balance
    output_path: full path (including filename) to write the .md file to
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    generated_on = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = []

    lines.append("# Meetup Tracker Report")
    lines.append("")
    lines.append(f"_Generated: {generated_on}_")
    lines.append("")

    lines.append("## Summary")
    lines.append("")
    lines.append(f"- **Total collected:** {totals['collected']:.2f}")
    lines.append(f"- **Total spent:** {totals['spent']:.2f}")
    lines.append(f"- **Remaining balance:** {totals['balance']:.2f}")
    lines.append("")

    lines.append("## Payments Collected")
    lines.append("")
    if payments:
        lines.append("| Name | Amount | Date |")
        lines.append("|---|---|---|")
        for p in payments:
            lines.append(f"| {p['name']} | {p['amount']:.2f} | {p['timestamp']} |")
    else:
        lines.append("_No payments recorded._")
    lines.append("")

    lines.append("## Expenses")
    lines.append("")
    if expenses:
        lines.append("| Item | Amount | Date |")
        lines.append("|---|---|---|")
        for e in expenses:
            lines.append(f"| {e['item']} | {e['amount']:.2f} | {e['timestamp']} |")
    else:
        lines.append("_No expenses recorded._")
    lines.append("")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return output_path


def get_report_filename():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"meetup_report_{timestamp}.md"
