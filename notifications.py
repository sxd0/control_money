import sqlite3
from collections import defaultdict
from datetime import datetime

DB_NAME = "expenses.db"

LIMITS = {
    "Кофе": 1000,
    "Еда": 5000,
    "Развлечения": 2000,
}

def check_spending_limits():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    current_month = datetime.now().strftime("%Y-%m")
    spending = defaultdict(float)

    cursor.execute('''
        SELECT expenses.amount, categories.name, expenses.date
        FROM expenses
        JOIN categories ON expenses.category_id = categories.id
    ''')

    for amount, category, date in cursor.fetchall():
        if date.startswith(current_month):
            spending[category] += amount

    conn.close()

    messages = []
    for category, limit in LIMITS.items():
        if spending[category] > limit:
            messages.append(f"Ты тратишь слишком много на {category.lower()}… как всегда.")

    return messages
