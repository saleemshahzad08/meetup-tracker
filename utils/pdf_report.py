"""
utils/pdf_report.py — builds a PDF summary of payments and expenses.

Deliberately text-only: no receipt images are embedded, per the brief.
This keeps the PDF small and focused purely on the money records.

No Kivy imports here, so it can be tested on its own.
"""

import os
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


def generate_pdf_report(payments, expenses, totals, output_path):
    """
    payments: list of dicts with keys name, amount, timestamp
    expenses: list of dicts with keys item, amount, timestamp
    totals: dict with keys collected, spent, balance
    output_path: full path (including filename) to write the PDF to
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
    )

    story = []

    story.append(Paragraph("Meetup Tracker Report", styles["Title"]))
    generated_on = datetime.now().strftime("%Y-%m-%d %H:%M")
    story.append(Paragraph(f"Generated: {generated_on}", styles["Normal"]))
    story.append(Spacer(1, 0.5 * cm))

    # ---- Summary ----
    story.append(Paragraph("Summary", styles["Heading2"]))
    summary_data = [
        ["Total collected", f"{totals['collected']:.2f}"],
        ["Total spent", f"{totals['spent']:.2f}"],
        ["Remaining balance", f"{totals['balance']:.2f}"],
    ]
    summary_table = Table(summary_data, colWidths=[6 * cm, 6 * cm])
    summary_table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 11),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("LINEBELOW", (0, 0), (-1, -2), 0.5, colors.lightgrey),
                ("FONTNAME", (0, 2), (-1, 2), "Helvetica-Bold"),
            ]
        )
    )
    story.append(summary_table)
    story.append(Spacer(1, 1 * cm))

    # ---- Payments ----
    story.append(Paragraph("Payments Collected", styles["Heading2"]))
    if payments:
        payment_rows = [["Name", "Amount", "Date"]]
        for p in payments:
            payment_rows.append([p["name"], f"{p['amount']:.2f}", p["timestamp"]])
        payment_table = Table(payment_rows, colWidths=[6 * cm, 4 * cm, 6 * cm])
        payment_table.setStyle(_table_style())
        story.append(payment_table)
    else:
        story.append(Paragraph("No payments recorded.", styles["Normal"]))
    story.append(Spacer(1, 1 * cm))

    # ---- Expenses ----
    story.append(Paragraph("Expenses", styles["Heading2"]))
    if expenses:
        expense_rows = [["Item", "Amount", "Date"]]
        for e in expenses:
            expense_rows.append([e["item"], f"{e['amount']:.2f}", e["timestamp"]])
        expense_table = Table(expense_rows, colWidths=[6 * cm, 4 * cm, 6 * cm])
        expense_table.setStyle(_table_style())
        story.append(expense_table)
    else:
        story.append(Paragraph("No expenses recorded.", styles["Normal"]))

    doc.build(story)
    return output_path


def _table_style():
    return TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#00695C")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F5F5F5")]),
        ]
    )


def get_report_filename():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"meetup_report_{timestamp}.pdf"
