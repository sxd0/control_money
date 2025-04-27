import sqlite3
from datetime import datetime

DB_NAME = "expenses.db"

def connect_db():
    return sqlite3.connect(DB_NAME)

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    # Таблица пользователей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE
        )
    ''')

    # Таблица категорий
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    ''')

    # Таблица способов оплаты
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payment_methods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            method_name TEXT NOT NULL UNIQUE
        )
    ''')

    # Таблица расходов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category_id INTEGER NOT NULL,
            payment_method_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (category_id) REFERENCES categories(id),
            FOREIGN KEY (payment_method_id) REFERENCES payment_methods(id)
        )
    ''')

    conn.commit()
    conn.close()

def add_user(username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO users (username) VALUES (?)', (username,))
    conn.commit()
    conn.close()

def add_category(name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO categories (name) VALUES (?)', (name,))
    conn.commit()
    conn.close()

def add_payment_method(method_name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO payment_methods (method_name) VALUES (?)', (method_name,))
    conn.commit()
    conn.close()

def get_user_id(username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def get_category_id(category_name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM categories WHERE name = ?', (category_name,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def get_payment_method_id(method_name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM payment_methods WHERE method_name = ?', (method_name,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def add_expense_to_db(user_id, category_id, payment_method_id, amount):
    conn = connect_db()
    cursor = conn.cursor()
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO expenses (user_id, category_id, payment_method_id, amount, date)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, category_id, payment_method_id, amount, date))
    conn.commit()
    conn.close()

def get_expenses():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT expenses.date, expenses.amount, categories.name, payment_methods.method_name
        FROM expenses
        JOIN categories ON expenses.category_id = categories.id
        JOIN payment_methods ON expenses.payment_method_id = payment_methods.id
    ''')
    expenses = cursor.fetchall()
    conn.close()
    return expenses

def get_all_payment_methods():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT method_name FROM payment_methods')
    methods = [row[0] for row in cursor.fetchall()]
    conn.close()
    return methods
