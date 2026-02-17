from config.categories import CATEGORIES, CATEGORY_DESCRIPTIONS


def build_batch_prompt(items):
    """
    items: list of tuples (id, description)
    """

    categories_text = "\n".join(
        [f"- {cat}: {CATEGORY_DESCRIPTIONS[cat]}" for cat in CATEGORIES]
    )

    transactions_text = "\n".join(
        [f'{item_id}: "{desc}"' for item_id, desc in items]
    )

    prompt = f"""
You are an expense categorization assistant.

Classify each transaction into ONE of the categories below.

Categories:
{categories_text}

Transactions:
{transactions_text}

Respond ONLY in valid JSON format:

{{
  "results": [
    {{
      "id": <transaction id>,
      "category": "<one category>",
      "confidence": <0 to 1>
    }}
  ]
}}
"""

    return prompt
