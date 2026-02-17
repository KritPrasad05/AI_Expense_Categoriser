import io
import pandas as pd
import matplotlib.pyplot as plt

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors, pagesizes
from reportlab.lib.styles import getSampleStyleSheet 
from reportlab.lib.units import inch

from core.report import monthly_spend_trend


def generate_csv_export(df: pd.DataFrame):
    output = io.StringIO()
    df.to_csv(output, index=False)
    return output.getvalue()

def create_category_chart(category_summary):
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(category_summary["category"], category_summary["amount"])
    ax.set_xticklabels(category_summary["category"], rotation=45)
    ax.set_ylabel("Total Spend")
    ax.set_title("Spend by Category")

    img_buffer = io.BytesIO()
    plt.tight_layout()
    plt.savefig(img_buffer, format="png")
    plt.close(fig)

    img_buffer.seek(0)
    return img_buffer
    
def create_monthly_trend_chart(monthly_data):
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(monthly_data["month"], monthly_data["amount"])
    ax.set_xticklabels(monthly_data["month"], rotation=45)
    ax.set_ylabel("Monthly Spend")
    ax.set_title("Monthly Spend Trend")

    img_buffer = io.BytesIO()
    plt.tight_layout()
    plt.savefig(img_buffer, format="png")
    plt.close(fig)

    img_buffer.seek(0)
    return img_buffer


def generate_pdf_report(df, metrics, category_summary, anomaly_data, top_transactions):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=pagesizes.A4)

    elements = []
    styles = getSampleStyleSheet()

    # Title
    elements.append(Paragraph("<b>AI Expense Categorization Report</b>", styles["Title"]))
    elements.append(Spacer(1, 0.3 * inch))

    # Summary Section
    elements.append(Paragraph("<b>Executive Summary</b>", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))

    summary_data = [
        ["Total Spend", f"₹ {metrics['total_spend']:,.2f}"],
        ["Total Transactions", metrics["total_transactions"]],
        ["Total Anomalies", metrics["total_anomalies"]],
    ]

    table = Table(summary_data)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 0.4 * inch))

    # Category Spend
    elements.append(Paragraph("<b>Spend by Category</b>", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))

    category_table_data = [["Category", "Total Spend", "%"]]
    for _, row in category_summary.iterrows():
        category_table_data.append([
            row["category"],
            f"₹ {row['amount']:,.2f}",
            f"{row['percentage']:.2f}%"
        ])

    cat_table = Table(category_table_data)
    cat_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))

    elements.append(cat_table)
    elements.append(Spacer(1, 0.4 * inch))

    # Category Chart
    elements.append(Spacer(1, 0.3 * inch))
    elements.append(Paragraph("<b>Category Spend Chart</b>", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))
    
    chart_buffer = create_category_chart(category_summary)
    elements.append(Image(chart_buffer, width=400, height=250))
    elements.append(Spacer(1, 0.4 * inch))

    # Anomaly Breakdown
    elements.append(Paragraph("<b>Anomaly Breakdown</b>", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))

    anomaly_table = Table([
        ["Category-based anomalies", anomaly_data["category_anomalies"]],
        ["Duplicate anomalies", anomaly_data["duplicate_anomalies"]],
        ["High absolute risk transactions", anomaly_data["high_absolute_risk"]],
    ])

    anomaly_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))

    elements.append(anomaly_table)
    elements.append(Spacer(1, 0.4 * inch))

    # Monthly Trend Chart
    elements.append(Paragraph("<b>Monthly Spend Trend</b>", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))
    
    monthly_data = monthly_spend_trend(df)
    trend_buffer = create_monthly_trend_chart(monthly_data)
    elements.append(Image(trend_buffer, width=400, height=250))
    elements.append(Spacer(1, 0.4 * inch))

    # Top Transactions
    elements.append(Paragraph("<b>Top 5 Largest Transactions</b>", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))

    top_data = [["Date", "Description", "Amount"]]

    for _, row in top_transactions.iterrows():
        top_data.append([
            str(row["date"]),
            row["description"],
            f"₹ {row['amount']:,.2f}"
        ])

    top_table = Table(top_data)
    top_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))

    elements.append(top_table)

    doc.build(elements)
    buffer.seek(0)

    return buffer