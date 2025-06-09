import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'inventory.db')

def init_caches_table():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS caches (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            description TEXT
        );
    """)
    # Add cache_id column to bars table if missing
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(bars);")
    cols = [row[1] for row in cur.fetchall()]
    if 'cache_id' not in cols:
        conn.execute("ALTER TABLE bars ADD COLUMN cache_id INTEGER REFERENCES caches(id);")
    conn.commit()
    conn.close()


def list_caches():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, name, latitude, longitude, description FROM caches;")
    rows = cur.fetchall()
    conn.close()
    return rows


def add_cache(name, latitude, longitude, description):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO caches (name, latitude, longitude, description) VALUES (?, ?, ?, ?)",
        (name, latitude, longitude, description)
    )
    conn.commit()
    conn.close()