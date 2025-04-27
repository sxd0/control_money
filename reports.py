import csv
from collections import defaultdict
from datetime import datetime

FILENAME = "expenses.csv"
REPORT_FILE = "monthly_report.txt"

def generate_monthly_report():
    if not csv_file_exists():
        return "Файл расходов не найден."

    expenses_by_category = defaultdict(float)
    total = 0.0

    current_month = datetime.now().strftime("%Y-%m")

    with open(FILENAME, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            date_str, amount_str, category = row
            if date_str.startswith(current_month):
                amount = float(amount_str)
                expenses_by_category[category] += amount
                total += amount

    with open(REPORT_FILE, "w", encoding="utf-8") as report:
        report.write(f"Отчёт за {current_month}\n")
        report.write(f"Общие расходы: {total:.2f} руб.\n\n")
        report.write("Расходы по категориям:\n")
        for category, amount in expenses_by_category.items():
            report.write(f" - {category}: {amount:.2f} руб.\n")

    return f"Отчёт создан: {REPORT_FILE}"

def csv_file_exists():
    import os
    return os.path.exists(FILENAME)
