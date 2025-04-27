import csv
from collections import defaultdict
from datetime import datetime

FILENAME = "expenses.csv"
LIMITS = {
    "Кофе": 1000,
    "Еда": 5000,
    "Развлечения": 2000,
    "Вредные привычки": 1000,
}

def check_spending_limits():
    current_month = datetime.now().strftime("%Y-%m")
    spending = defaultdict(float)

    try:
        with open(FILENAME, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                date_str, amount_str, category = row
                if date_str.startswith(current_month):
                    amount = float(amount_str)
                    spending[category] += amount
    except FileNotFoundError:
        return []

    messages = []
    for category, limit in LIMITS.items():
        if spending[category] > limit:
            messages.append(f"Ты тратишь слишком много на {category.lower()}… как всегда.......")

    return messages
