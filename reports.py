import sqlite3
from collections import defaultdict
from datetime import datetime

DB_NAME = "expenses.db"
REPORT_FILE = "monthly_report.txt"

def generate_monthly_report():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    current_month = datetime.now().strftime("%Y-%m")
    expenses_by_category = defaultdict(float)
    expenses_by_payment_method = defaultdict(float)
    total = 0.0

    cursor.execute('''
        SELECT expenses.amount, categories.name, payment_methods.method_name, expenses.date
        FROM expenses
        JOIN categories ON expenses.category_id = categories.id
        JOIN payment_methods ON expenses.payment_method_id = payment_methods.id
    ''')

    for amount, category, payment_method, date in cursor.fetchall():
        if date.startswith(current_month):
            expenses_by_category[category] += amount
            expenses_by_payment_method[payment_method] += amount
            total += amount

    conn.close()

    with open(REPORT_FILE, "w", encoding="utf-8") as report:
        report.write(f"Отчёт за {current_month}\n")
        report.write(f"Общие расходы: {total:.2f} руб.\n\n")

        report.write("Расходы по категориям:\n")
        for category, amount in expenses_by_category.items():
            report.write(f" - {category}: {amount:.2f} руб.\n")

        report.write("\nРасходы по способам оплаты:\n")
        for method, amount in expenses_by_payment_method.items():
            report.write(f" - {method}: {amount:.2f} руб.\n")

    return f"Отчёт создан: {REPORT_FILE}"
