import sqlite3
from typing import List, Optional, Tuple, Dict
import hashlib
import datetime

DB_NAME = 'korzinka.db'

# --- Инициализация базы данных ---
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Таблица товаров
    c.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            barcode TEXT,
            production_date TEXT NOT NULL,
            expiry_date TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            remind_date TEXT NOT NULL,
            status TEXT NOT NULL
        )
    ''')
    # Таблица пользователей
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# --- Класс для работы с товарами ---
class ProductDB:
    def __init__(self, db_name=DB_NAME):
        self.db_name = db_name

    def add_product(self, name: str, barcode: Optional[str], production_date: str, expiry_date: str, quantity: int, remind_date: str, status: str = 'on_shelf'):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('''
            INSERT INTO products (name, barcode, production_date, expiry_date, quantity, remind_date, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, barcode, production_date, expiry_date, quantity, remind_date, status))
        conn.commit()
        conn.close()

    def get_all_products(self) -> List[Tuple]:
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('SELECT * FROM products WHERE status = "on_shelf"')
        rows = c.fetchall()
        conn.close()
        return rows

    def get_expired_products(self, today: str) -> List[Tuple]:
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('SELECT * FROM products WHERE expiry_date < ? AND status = "on_shelf"', (today,))
        rows = c.fetchall()
        conn.close()
        return rows

    def remove_products(self, ids: List[int]):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.executemany('UPDATE products SET status = "removed" WHERE id = ?', [(i,) for i in ids])
        conn.commit()
        conn.close()

    def get_removed_products(self) -> List[Tuple]:
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('SELECT * FROM products WHERE status = "removed"')
        rows = c.fetchall()
        conn.close()
        return rows

    def get_all_product_names(self) -> list:
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('SELECT DISTINCT name FROM products')
        names = [row[0] for row in c.fetchall()]
        conn.close()
        return names

    def get_barcode_by_name(self, name: str) -> Optional[str]:
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('SELECT barcode FROM products WHERE name = ? AND barcode IS NOT NULL AND barcode != "" LIMIT 1', (name,))
        row = c.fetchone()
        conn.close()
        return row[0] if row else None

    def get_products_expiring_soon(self, today: str, days: int) -> List[Tuple]:
        """
        Возвращает товары, срок годности которых истекает через N дней (включительно).
        today: дата в формате 'yyyy-MM-dd'
        days: количество дней до истечения срока
        """
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        # today в формате 'yyyy-MM-dd'
        start_date = today
        end_date = (datetime.datetime.strptime(today, '%Y-%m-%d') + datetime.timedelta(days=days)).strftime('%Y-%m-%d')
        c.execute('''
            SELECT * FROM products WHERE expiry_date >= ? AND expiry_date <= ? AND status = "on_shelf"
        ''', (start_date, end_date))
        rows = c.fetchall()
        conn.close()
        return rows

# --- Класс для работы с пользователями ---
class UserDB:
    def __init__(self, db_name=DB_NAME):
        self.db_name = db_name

    def add_user(self, username: str, password: str, role: str):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        hashed = hashlib.sha256(password.encode()).hexdigest()
        c.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', (username, hashed, role))
        conn.commit()
        conn.close()

    def authenticate(self, username: str, password: str) -> Optional[Dict]:
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        hashed = hashlib.sha256(password.encode()).hexdigest()
        c.execute('SELECT id, username, role FROM users WHERE username = ? AND password = ?', (username, hashed))
        row = c.fetchone()
        conn.close()
        if row:
            return {'id': row[0], 'username': row[1], 'role': row[2]}
        return None

    def get_all_users(self) -> List[Tuple]:
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('SELECT id, username, role FROM users')
        rows = c.fetchall()
        conn.close()
        return rows

    def delete_user(self, user_id: int):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()

    def change_password(self, user_id: int, new_password: str):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        hashed = hashlib.sha256(new_password.encode()).hexdigest()
        c.execute('UPDATE users SET password = ? WHERE id = ?', (hashed, user_id))
        conn.commit()
        conn.close()

    def authenticate_by_id(self, user_id: int, password: str) -> Optional[Dict]:
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        hashed = hashlib.sha256(password.encode()).hexdigest()
        c.execute('SELECT id, username, role FROM users WHERE id = ? AND password = ?', (user_id, hashed))
        row = c.fetchone()
        conn.close()
        if row:
            return {'id': row[0], 'username': row[1], 'role': row[2]}
        return None 