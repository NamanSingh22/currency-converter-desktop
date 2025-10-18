import os
import sqlite3
import datetime

DB_DIR= os.path.join(os.getcwd(), ".data")
os.makedirs(DB_DIR, exist_ok=True)

DB_NAME = os.path.join(DB_DIR, "rates_cache.db")

class RateCache:
    def __init__(self, db_name = DB_NAME):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        self.conn.execute("""
                CREATE TABLE IF NOT EXISTS rates_cache(
                base TEXT,
                target TEXT,
                rate REAL,
                date TEXT,
                PRIMARY KEY (base, target)
                )"""
            )
        self.conn.commit()


    def get_all_rates(self, base="USD"):
        cur = self.conn.cursor()
        today = datetime.date.today().isoformat()
        cur.execute("SELECT target, rate FROM rates_cache WHERE base=? AND date = ?",(base,today,))
        rows = cur.fetchall()
        return {
            c: r for c, r in rows
        } if rows else None

    def get_any_rates(self, base="USD"):
        """Return any rates stored in DB (useful as offline fallback)."""
        cur = self.conn.cursor()
        cur.execute("SELECT target, rate FROM rates_cache WHERE base=?", (base,))
        rows = cur.fetchall()
        return {c: r for c, r in rows} if rows else None


    def save_rates(self,base,rates):
        today = datetime.date.today().isoformat()
        cur = self.conn.cursor()
        for target, rate in rates.items():
            cur.execute( """
                REPLACE INTO rates_cache (base, target, rate, date) VALUES (?,?,?,?) """,
                (base, target, rate, today))
        self.conn.commit()
        

    def clear_old(self):
        today = datetime.date.today().isoformat()
        self.conn.execute("DELETE FROM rates_cache WHERE date <> ?", (today,))
        self.conn.commit()

    def close(self):
        self.conn.close()
    
