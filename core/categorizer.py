from config.categories import CATEGORIES

import json
import pandas as pd
from llm.prompt_builder import build_batch_prompt
from llm.groq_client import call_groq
from llm.schemas import BatchCategorization


# Merchant keyword mapping
RULE_BASED_KEYWORDS = {
    "Travel": ["uber", "ola", "air india", "indigo", "marriott"],
    "Meals": ["starbucks", "mcdonald", "dominos", "kfc", "restaurant"],
    "Software": ["aws", "google cloud", "notion", "slack", "adobe"],
    "Utilities": ["electricity", "vodafone", "airtel", "internet"],
    "Marketing": ["facebook ads", "google ads", "linkedin ads"],
    "Office Supplies": ["amazon", "staples", "flipkart"],
    "Entertainment": ["netflix", "spotify", "bookmyshow"],
    "Healthcare": ["apollo", "pharmacy"]
}

def rule_based_categorize(description: str):
    desc_lower = description.lower()

    for category, keywords in RULE_BASED_KEYWORDS.items():
        for keyword in keywords:
            if keyword in desc_lower:
                return category, 1.0  # Full confidence

    return None, 0.0

def llm_batch_categorize(batch_items):
    prompt = build_batch_prompt(batch_items)
    response = call_groq(prompt)

    try:
        parsed = json.loads(response)
        validated = BatchCategorization(**parsed)
        return validated.results
    except Exception as e:
        print("LLM Parsing Error:", e)
        return []


def hybrid_categorize(description: str):
    category, confidence = rule_based_categorize(description)

    if category:
        return category, confidence, "rule_based"

    llm_category, llm_confidence = llm_categorize(description)
    return llm_category, llm_confidence, "llm"


def categorize_dataframe(df: pd.DataFrame, batch_size: int = 20) -> pd.DataFrame:
    df = df.copy()

    df["category"] = None
    df["confidence"] = 0.0
    df["classification_source"] = None

    llm_candidates = []

    # First pass: rule-based
    for idx, row in df.iterrows():
        category, confidence = rule_based_categorize(row["description"])

        if category:
            df.at[idx, "category"] = category
            df.at[idx, "confidence"] = confidence
            df.at[idx, "classification_source"] = "rule_based"
        else:
            llm_candidates.append((idx, row["description"]))

    # Batch LLM calls
    for i in range(0, len(llm_candidates), batch_size):
        batch = llm_candidates[i:i + batch_size]

        results = llm_batch_categorize(batch)

        for result in results:
            idx = result.id
            df.at[idx, "category"] = result.category
            df.at[idx, "confidence"] = result.confidence
            df.at[idx, "classification_source"] = "llm"

    # Fallback safety
    df["category"] = df["category"].fillna("Other")
    df["classification_source"] = df["classification_source"].fillna("fallback")

    return df
