import streamlit as st
import matplotlib.pyplot as plt

from core.validator import validate_and_load, CSVValidationError
from core.preprocessing import preprocess_dataframe
from core.categorizer import categorize_dataframe
from core.anomaly import apply_anomaly_detection
from core.report import (
    generate_summary_metrics,
    spend_by_category,
    top_5_largest_transactions,
    anomaly_breakdown,
    monthly_spend_trend,
    average_spend_per_category
)
from core.exporter import generate_csv_export, generate_pdf_report

st.set_page_config(page_title="AI Expense Categorizer")

st.title("AI Expense Categorizer")

uploaded_file = st.file_uploader("Upload Expense CSV", type=["csv"])

if uploaded_file:
    try:
        df = validate_and_load(uploaded_file)
        df = preprocess_dataframe(df)

        st.success("File processed successfully!")

        with st.spinner("Categorizing expenses..."):
            df = categorize_dataframe(df)

        st.subheader("Categorized Data")
        st.dataframe(df.head(100))
        st.write(df["classification_source"].value_counts())

        with st.spinner("Detecting anomalies..."):
            df = apply_anomaly_detection(df)
        
        st.subheader("Anomaly Summary")
        st.write(df["anomaly_flag"].value_counts())
        
        st.subheader("Anomalies Detected")
        st.dataframe(df[df["anomaly_flag"] == True])

        st.header("Executive Summary Dashboard")
        
        # --- Metrics ---
        metrics = generate_summary_metrics(df)
        
        col1, col2, col3 = st.columns(3)
        
        col1.metric("Total Spend", f"₹ {metrics['total_spend']:,.2f}")
        col2.metric("Total Transactions", metrics["total_transactions"])
        col3.metric("Total Anomalies", metrics["total_anomalies"])
        
        # --- Spend by Category ---
        st.subheader("Spend by Category")
        
        category_summary = spend_by_category(df)
        st.dataframe(category_summary)
        
        # Bar Chart
        fig, ax = plt.subplots()
        ax.bar(category_summary["category"], category_summary["amount"])
        ax.set_xticklabels(category_summary["category"], rotation=45)
        ax.set_ylabel("Total Spend")
        st.pyplot(fig)
        
        # --- Top 5 Largest Transactions ---
        st.subheader("Top 5 Largest Transactions")
        st.dataframe(top_5_largest_transactions(df))
        
        # --- Anomaly Breakdown ---
        st.subheader("Anomaly Breakdown")
        breakdown = anomaly_breakdown(df)
        
        st.write(f"Category-based anomalies: {breakdown['category_anomalies']}")
        st.write(f"Duplicate anomalies: {breakdown['duplicate_anomalies']}")
        st.write(f"High absolute risk transactions: {breakdown['high_absolute_risk']}")
        
        # --- Monthly Trend ---
        st.subheader("Monthly Spend Trend")
        
        monthly = monthly_spend_trend(df)
        
        fig2, ax2 = plt.subplots()
        ax2.plot(monthly["month"], monthly["amount"])
        ax2.set_xticklabels(monthly["month"], rotation=45)
        ax2.set_ylabel("Monthly Spend")
        st.pyplot(fig2)
        
        # --- Average Spend Per Category ---
        st.subheader("Average Spend per Category")
        st.dataframe(average_spend_per_category(df))

        st.header("Export Reports")

        # CSV Export
        csv_data = generate_csv_export(df)
        
        st.download_button(
            label="Download Processed CSV",
            data=csv_data,
            file_name="processed_expense_report.csv",
            mime="text/csv"
        )
        
        # PDF Export
        pdf_buffer = generate_pdf_report(
            df,
            metrics,
            category_summary,
            breakdown,
            top_5_largest_transactions(df)
        )
        
        st.download_button(
            label="Download PDF Report",
            data=pdf_buffer,
            file_name="expense_report.pdf",
            mime="application/pdf"
        )
        
    except CSVValidationError as e:
        st.error(str(e))

    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
