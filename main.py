import tkinter as tk
from tkinter import messagebox, ttk
from database import (
    create_tables, add_user, add_category, add_payment_method,
    get_user_id, get_category_id, get_payment_method_id,
    add_expense_to_db, get_expenses, get_all_payment_methods
)
from notifications import check_spending_limits
from reports import generate_monthly_report

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Трекер расходов")

        create_tables()
        add_user("default_user")
        for method in ["Наличные", "Банковская карта", "Онлайн-платеж"]:
            add_payment_method(method)

        self.amount_label = tk.Label(root, text="Сумма:")
        self.amount_label.grid(row=0, column=0)
        self.amount_entry = tk.Entry(root)
        self.amount_entry.grid(row=0, column=1)

        self.category_label = tk.Label(root, text="Категория:")
        self.category_label.grid(row=1, column=0)
        self.category_entry = tk.Entry(root)
        self.category_entry.grid(row=1, column=1)

        self.payment_label = tk.Label(root, text="Способ оплаты:")
        self.payment_label.grid(row=2, column=0)
        self.payment_var = tk.StringVar()
        self.payment_combobox = ttk.Combobox(root, textvariable=self.payment_var, state="readonly")
        self.payment_combobox['values'] = get_all_payment_methods()
        self.payment_combobox.grid(row=2, column=1)

        self.add_button = tk.Button(root, text="Добавить", command=self.add_expense)
        self.add_button.grid(row=3, column=0, columnspan=2)

        self.report_button = tk.Button(root, text="Сформировать отчет", command=self.show_report)
        self.report_button.grid(row=3, column=2, padx=10)

        self.expenses_tree = ttk.Treeview(root, columns=("Дата", "Сумма", "Категория", "Способ оплаты"), show="headings")
        self.expenses_tree.heading("Дата", text="Дата")
        self.expenses_tree.heading("Сумма", text="Сумма")
        self.expenses_tree.heading("Категория", text="Категория")
        self.expenses_tree.heading("Способ оплаты", text="Способ оплаты")
        self.expenses_tree.grid(row=4, columnspan=3)

        self.load_expenses()

    def add_expense(self):
        amount = self.amount_entry.get()
        category = self.category_entry.get()
        payment_method = self.payment_var.get()

        if not amount or not category or not payment_method:
            messagebox.showwarning("Ошибка", "Заполните все поля")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showwarning("Ошибка", "Сумма должна быть числом")
            return

        add_category(category)
        user_id = get_user_id("default_user")
        category_id = get_category_id(category)
        payment_method_id = get_payment_method_id(payment_method)

        add_expense_to_db(user_id, category_id, payment_method_id, amount)

        self.expenses_tree.insert("", "end", values=(tk.StringVar().get(), amount, category, payment_method))
        self.amount_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.payment_combobox.set("")

        warnings = check_spending_limits()
        if warnings:
            messagebox.showwarning("Уведомление", "\n".join(warnings))

    def load_expenses(self):
        expenses = get_expenses()
        for date, amount, category, payment_method in expenses:
            self.expenses_tree.insert("", "end", values=(date, amount, category, payment_method))

    def show_report(self):
        message = generate_monthly_report()
        messagebox.showinfo("Отчёт", message)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
