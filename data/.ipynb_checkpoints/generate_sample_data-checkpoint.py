import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def random_date():
    start = datetime(2024, 1, 1).date()
    end = datetime.now().date()
    return start + timedelta(days=random.randint(0, (end - start).days))

# Category distributions (mean, std)
category_distributions = {
    "Travel": (8000, 1500),
    "Meals": (1200, 300),
    "Software": (5000, 1000),
    "Utilities": (3000, 500),
    "Marketing": (15000, 3000),
    "Office Supplies": (4000, 800),
    "Entertainment": (2000, 400),
    "Healthcare": (6000, 1200),
}

category_merchants = {
    "Travel": ["Uber", "Air India", "Marriott Hotel"],
    "Meals": ["Starbucks", "Dominos"],
    "Software": ["Adobe", "AWS", "Notion"],
    "Utilities": ["Airtel", "Electricity Board"],
    "Marketing": ["Facebook Ads", "Google Ads"],
    "Office Supplies": ["Amazon", "Staples"],
    "Entertainment": ["Netflix", "Spotify"],
    "Healthcare": ["Apollo Hospital"],
}

twisted_names = [
    "UBER TRIP #3921",
    "AMZN MKTP",
    "SPOTIFY AB",
    "AIR TEL LTD",
    "ADOBE*SUB",
    "NETFLIX.COM",
    "FB ADS 2391",
    "Apollo Hlth Srvs",
]

rows = []

# 160 normal transactions
for _ in range(160):
    category = random.choice(list(category_distributions.keys()))
    mean, std = category_distributions[category]

    amount = max(100, np.random.normal(mean, std))

    merchant = random.choice(category_merchants[category])

    # 50% chance to twist name
    if random.random() < 0.5:
        merchant = random.choice(twisted_names)

    rows.append({
        "date": random_date().strftime("%Y-%m-%d"),
        "amount": round(amount, 2),
        "description": merchant
    })


# 10 category anomalies (extreme within category)
for _ in range(10):
    category = random.choice(list(category_distributions.keys()))
    mean, std = category_distributions[category]

    # 5x typical value → should trigger Z-score
    amount = mean + (5 * std)

    merchant = random.choice(category_merchants[category])

    rows.append({
        "date": random_date().strftime("%Y-%m-%d"),
        "amount": round(amount, 2),
        "description": merchant
    })


# 10 global extreme anomalies
for _ in range(10):
    rows.append({
        "date": random_date().strftime("%Y-%m-%d"),
        "amount": random.randint(120000, 300000),
        "description": "Unknown International Transfer"
    })


# 10 duplicates
duplicate_entry = {
    "date": "2024-06-15",
    "amount": 4999.99,
    "description": "Amazon"
}

for _ in range(10):
    rows.append(duplicate_entry)


# 10 ambiguous random entries
for _ in range(10):
    rows.append({
        "date": random_date().strftime("%Y-%m-%d"),
        "amount": random.randint(2000, 10000),
        "description": "Misc Vendor XYZ"
    })


df = pd.DataFrame(rows)
df.to_csv("data/anomaly_test_200.csv", index=False)

print("Anomaly test dataset (200 rows) generated successfully!")