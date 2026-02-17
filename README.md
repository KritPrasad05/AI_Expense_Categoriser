# AI Expense Categorizer

An AI-powered expense processing system that automates expense
categorization, anomaly detection, and executive reporting using Python,
Streamlit, Pandas, and a modern LLM (Groq API).

------------------------------------------------------------------------

## 🚀 Features

### 1. CSV Ingestion & Validation

-   Upload expense CSV files
-   Required columns: `date`, `amount`, `description`
-   Handles malformed rows and type coercion
-   Robust error handling with clear user-facing messages

### 2. Hybrid Expense Categorization

-   Rule-based keyword classification (fast, deterministic)
-   Batched LLM fallback classification (Groq API)
-   Structured JSON validation using Pydantic
-   Confidence score per classification
-   Classification source tracking (rule_based / llm)

### 3. Statistical Anomaly Detection

-   Category-based Z-score anomaly detection
-   Duplicate transaction detection
-   High absolute risk tagging (global extreme values)
-   Clear human-readable anomaly explanations

### 4. Executive Dashboard

-   Total Spend
-   Total Transactions
-   Total Anomalies
-   Spend by Category (table + bar chart)
-   Top 5 Largest Transactions
-   Anomaly Breakdown by Type
-   Monthly Spend Trend (line chart)
-   Average Spend per Category

### 5. Export Capabilities

-   Download processed CSV report
-   Generate professional PDF report including:
    -   Executive summary
    -   Category distribution
    -   Anomaly breakdown
    -   Top 5 transactions
    -   Embedded charts

------------------------------------------------------------------------

## 🏗️ Architecture

Pipeline:

CSV Upload\
→ Validation\
→ Preprocessing\
→ Hybrid Categorization (Rule + LLM Batch)\
→ Statistical Anomaly Detection\
→ Executive Summary Report\
→ Export (CSV / PDF)

Modular Structure:

    ai_expense_categorizer/
    │
    ├── app.py
    ├── core/
    │   ├── validator.py
    │   ├── preprocessing.py
    │   ├── categorizer.py
    │   ├── anomaly.py
    │   ├── report.py
    │   └── exporter.py
    │
    ├── llm/
    │   ├── groq_client.py
    │   ├── prompt_builder.py
    │   └── schemas.py
    │
    ├── config/
    │   └── categories.py
    │
    ├── data/
    └── utils/

------------------------------------------------------------------------

## 🧠 Technical Highlights

-   Batched LLM classification to avoid API rate limits
-   Structured output enforcement using Pydantic schemas
-   Category-level statistical anomaly detection using Z-score
-   Separation of risk tagging and anomaly classification
-   Fully modular, production-style architecture

------------------------------------------------------------------------

## 🛠️ Setup Instructions

### 1. Create Virtual Environment

``` bash
python -m venv expense-ai-env
expense-ai-env\Scripts\activate  # Windows
```

### 2. Install Dependencies

``` bash
pip install -r requirements.txt
```

### 3. Set API Key

Create `.env` file:

    GROQ_API_KEY=your_api_key_here

### 4. Run Application

``` bash
streamlit run app.py
```

------------------------------------------------------------------------

## 📊 Sample Data

Synthetic datasets were generated to simulate: - Normal transactions -
Twisted merchant names - Category-based anomalies - Duplicate entries -
Extreme global transfers

------------------------------------------------------------------------

## ⚠ Limitations

-   LLM performance depends on external API availability
-   Z-score anomaly detection assumes near-normal distribution per
    category
-   Designed for moderate dataset sizes (can be scaled with batching
    optimizations)

------------------------------------------------------------------------

## 📌 Future Improvements

-   Editable category configuration from UI
-   Persistent storage (database integration)
-   Role-based access control
-   Advanced fraud detection models
-   Deployment to cloud infrastructure

------------------------------------------------------------------------

## 👤 Author

AI Expense Categorizer -- Technical Assessment Submission
