import sqlite3
import datetime
import csv
import os

DB_DIR= os.path.join(os.getcwd(), ".data")
os.makedirs(DB_DIR, exist_ok=True)

DB_NAME = os.path.join(DB_DIR, "currency_history.db")

class Database:
    def __init__(self, db_name=DB_NAME):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS history(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL,
                from_currency TEXT,
                to_currency TEXT,
                result REAL,
                timestamp TEXT
            )
            """
        )

        self.conn.commit()

    def save_conversion(self, amount, from_currency, to_currency, result):
        now_datetime = datetime.datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
        self.cursor.execute(
            "INSERT INTO history (amount, from_currency, to_currency, result, timestamp) VALUES (?,?,?,?,?)", (
                amount, from_currency, to_currency, result, now_datetime)
        )

        self.conn.commit()

    def fetch_history(self, limit=50):
        self.cursor.execute(
            "SELECT amount, from_currency, to_currency, result, timestamp FROM history ORDER BY id DESC LIMIT ?", (
                limit,)
        )
        return self.cursor.fetchall()

    def clear_history(self):
        self.cursor.execute("DELETE FROM history")
        self.conn.commit()
