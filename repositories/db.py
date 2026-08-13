import sqlite3

DB_PATH = "inventory.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items(
            item_id TEXT PRIMARY KEY,
            item_name TEXT NOT NULL,
            category TEXT NOT NULL,
            unit TEXT NOT NULL,
            reorder_level REAL NOT NULL,
            supplier TEXT,
            cost_per_unit REAL,
            storage_location TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory_entries (
            entry_id TEXT PRIMARY KEY,
            item_id TEXT NOT NULL REFERENCES items(item_id),
            quantity_on_hand REAL NOT NULL,
            last_updated TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movements (
            movement_id TEXT PRIMARY KEY,
            item_id TEXT NOT NULL REFERENCES items(item_id),
            quantity REAL NOT NULL,
            timestamp TEXT NOT NULL,
            movement_type TEXT NOT NULL,
            supplier TEXT,
            unit_cost REAL,
            total_cost REAL,
            expiry_date TEXT,
            note TEXT
        )
    """)

    conn.commit()
    conn.close()
