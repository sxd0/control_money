import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os
from datetime import datetime

from notifications import check_spending_limits
from reports import generate_monthly_report


FILENAME = "expenses.csv"

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Трекер расходов")

        self.amount_label = tk.Label(root, text="Сумма:")
        self.amount_label.grid(row=0, column=0)
        self.amount_entry = tk.Entry(root)
        self.amount_entry.grid(row=0, column=1)

        self.category_label = tk.Label(root, text="Категория:")
        self.category_label.grid(row=1, column=0)
        self.category_entry = tk.Entry(root)
        self.category_entry.grid(row=1, column=1)

        self.add_button = tk.Button(root, text="Добавить", command=self.add_expense)
        self.add_button.grid(row=2, columnspan=2)

        self.report_button = tk.Button(root, text="Сформировать отчёт", command=self.show_report)
        self.report_button.grid(row=2, column=2, padx=10)

        self.expenses_tree = ttk.Treeview(root, columns=("Дата", "Сумма", "Категория"), show="headings")
        self.expenses_tree.heading("Дата", text="Дата")
        self.expenses_tree.heading("Сумма", text="Сумма")
        self.expenses_tree.heading("Категория", text="Категория")
        self.expenses_tree.grid(row=3, columnspan=2)

        self.load_expenses()

    def add_expense(self):
        amount = self.amount_entry.get()
        category = self.category_entry.get()
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if not amount or not category:
            messagebox.showwarning("Ошибка", "Заполните все поля")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showwarning("Ошибка", "Сумма должна быть числом")
            return

        with open(FILENAME, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([date, amount, category])

        self.expenses_tree.insert("", "end", values=(date, amount, category))
        self.amount_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        warnings = check_spending_limits()
        if warnings:
            messagebox.showwarning("Уведомление", "\n".join(warnings))


    def load_expenses(self):
        if os.path.exists(FILENAME):
            with open(FILENAME, newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                for row in reader:
                    self.expenses_tree.insert("", "end", values=row)

    def show_report(self):
        message = generate_monthly_report()
        messagebox.showinfo("Отчёт", message)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
