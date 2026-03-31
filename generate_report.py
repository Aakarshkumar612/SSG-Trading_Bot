# generate_report.py — Generates PDF + CSV trade summary report

import os
import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table,
    TableStyle, HRFlowable
)

def generate_pdf_report(trade_log: list, order_manager):
    os.makedirs("reports", exist_ok=True)

    date_str  = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    pdf_path  = f"reports/SSG_Trade_Report_{date_str}.pdf"
    doc       = SimpleDocTemplate(pdf_path, pagesize=A4,
                                  topMargin=1.5*cm, bottomMargin=1.5*cm,
                                  leftMargin=2*cm, rightMargin=2*cm)

    styles    = getSampleStyleSheet()
    story     = []

    # ── Header ────────────────────────────────────────────────────
    title_style = ParagraphStyle("title",
        fontSize=22, fontName="Helvetica-Bold",
        textColor=colors.HexColor("#1a1a2e"), spaceAfter=4)
    sub_style = ParagraphStyle("sub",
        fontSize=11, fontName="Helvetica",
        textColor=colors.HexColor("#555555"), spaceAfter=2)

    story.append(Paragraph("SSG Trading Bot", title_style))
    story.append(Paragraph("AI-Powered Trade Summary Report", sub_style))
    story.append(Paragraph(
        f"Generated: {datetime.datetime.now().strftime('%d %B %Y, %I:%M %p')}",
        sub_style))
    story.append(HRFlowable(width="100%", thickness=2,
                            color=colors.HexColor("#1a1a2e"), spaceAfter=16))

    # ── Summary Stats ─────────────────────────────────────────────
    wins      = sum(1 for t in trade_log if t["result"] == "WIN")
    losses    = sum(1 for t in trade_log if t["result"] == "LOSS")
    total     = len(trade_log)
    win_rate  = round((wins / total) * 100, 1) if total > 0 else 0
    final_pnl = order_manager.total_pnl
    buys      = sum(1 for t in trade_log if t["type"] == "BUY")
    sells     = sum(1 for t in trade_log if t["type"] == "SELL")

    heading_style = ParagraphStyle("h2",
        fontSize=13, fontName="Helvetica-Bold",
        textColor=colors.HexColor("#1a1a2e"), spaceAfter=8)

    story.append(Paragraph("Performance Summary", heading_style))

    summary_data = [
        ["Metric", "Value"],
        ["Total Trades",       str(total)],
        ["Winning Trades",     f"{wins}"],
        ["Losing Trades",      f"{losses}"],
        ["Win Rate",           f"{win_rate}%"],
        ["Final P&L",          f"Rs. {final_pnl}"],
        ["BUY Trades",         str(buys)],
        ["SELL Trades",        str(sells)],
    ]

    summary_table = Table(summary_data, colWidths=[8*cm, 8*cm])
    summary_table.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, 0), colors.HexColor("#1a1a2e")),
        ("TEXTCOLOR",    (0, 0), (-1, 0), colors.white),
        ("FONTNAME",     (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",     (0, 0), (-1, 0), 11),
        ("ALIGN",        (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME",     (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE",     (0, 1), (-1, -1), 10),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
            [colors.HexColor("#f0f4ff"), colors.white]),
        ("GRID",         (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
        ("TOPPADDING",   (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 8),
    ]))

    story.append(summary_table)
    story.append(Spacer(1, 20))

    # ── Trade Log Table ───────────────────────────────────────────
    story.append(Paragraph("Detailed Trade Log", heading_style))

    table_data = [["#", "Type", "Entry", "Exit", "P&L", "Result", "Time"]]
    for t in trade_log:
        pnl_str = f"+Rs.{t['pnl']}" if t['pnl'] > 0 else f"-Rs.{abs(t['pnl'])}"
        table_data.append([
            str(t["trade_no"]),
            t["type"],
            f"Rs. {t['entry']}",
            f"Rs. {t['exit']}",
            pnl_str,
            t["result"],
            t["time"]
        ])

    col_widths = [1.2*cm, 2*cm, 3*cm, 3*cm, 2.5*cm, 2*cm, 2.5*cm]
    trade_table = Table(table_data, colWidths=col_widths, repeatRows=1)

    trade_style = TableStyle([
        ("BACKGROUND",   (0, 0), (-1, 0), colors.HexColor("#1a1a2e")),
        ("TEXTCOLOR",    (0, 0), (-1, 0), colors.white),
        ("FONTNAME",     (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",     (0, 0), (-1, -1), 8),
        ("ALIGN",        (0, 0), (-1, -1), "CENTER"),
        ("GRID",         (0, 0), (-1, -1), 0.4, colors.HexColor("#dddddd")),
        ("TOPPADDING",   (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 5),
    ])

    # Colour WIN rows green, LOSS rows red
    for i, row in enumerate(table_data[1:], start=1):
        if row[5] == "WIN":
            trade_style.add("BACKGROUND", (0, i), (-1, i),
                            colors.HexColor("#e6f9ec"))
        else:
            trade_style.add("BACKGROUND", (0, i), (-1, i),
                            colors.HexColor("#fdecea"))

    trade_table.setStyle(trade_style)
    story.append(trade_table)
    story.append(Spacer(1, 20))

    # ── Footer ────────────────────────────────────────────────────
    footer_style = ParagraphStyle("footer",
        fontSize=8, textColor=colors.grey, alignment=1)
    story.append(HRFlowable(width="100%", thickness=1,
                            color=colors.grey, spaceAfter=6))
    story.append(Paragraph(
        "SSG Assessment Project | AI-Powered Stock Trading Bot | Confidential",
        footer_style))

    doc.build(story)
    print(f"📄 PDF report saved → {pdf_path}")