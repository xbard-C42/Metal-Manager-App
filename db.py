import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'inventory.db')

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS bars (
            id INTEGER PRIMARY KEY,
            weight REAL NOT NULL,
            purity REAL NOT NULL,
            location TEXT NOT NULL,
            acquired DATE NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_bar(weight, purity, location):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO bars (weight, purity, location, acquired) VALUES (?, ?, ?, DATE('now'))",
        (weight, purity, location)
    )
    conn.commit()
    conn.close()

def list_bars():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, weight, purity, location, acquired FROM bars")
    rows = cur.fetchall()
    conn.close()
    return rows
