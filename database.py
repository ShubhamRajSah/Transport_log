import sqlite3

def init_db():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    
    # Create archive_entries table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS archive_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            loading_date TEXT,
            transport_name TEXT,
            vehicle_no TEXT,
            weight_slip TEXT,
            material TEXT,
            unloading_date TEXT,
            net_weight REAL,
            rate REAL,
            advance REAL,
            remaining_balance REAL,
            deleted INTEGER DEFAULT 0
        )
    """)

    # --- Create transport_entries table with soft delete support ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transport_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            loading_date TEXT,
            transport_name TEXT,
            vehicle_no TEXT,
            weight_slip TEXT,
            material TEXT,
            unloading_date TEXT,
            net_weight REAL,
            rate REAL,
            advance REAL,
            remaining_balance REAL,
            deleted INTEGER DEFAULT 0
        )
    """)

    # --- Create users table (optional login system) ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    conn.commit()
    conn.close()

# --- Soft delete an entry (mark as deleted) ---
def soft_delete_entry(entry_id):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE transport_entries SET deleted = 1 WHERE id = ?", (entry_id,))
    conn.commit()
    conn.close()

# --- Restore a deleted entry ---
def restore_entry(entry_id):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE transport_entries SET deleted = 0 WHERE id = ?", (entry_id,))
    conn.commit()
    conn.close()

# --- Archive all active entries ---
def archive_all_entries():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    # Create archive table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS archive_entries AS
        SELECT * FROM transport_entries WHERE 0
    """)

    # Copy active entries to archive
    cursor.execute("""
        INSERT INTO archive_entries
        SELECT * FROM transport_entries WHERE deleted = 0
    """)

    # Clear active entries
    cursor.execute("DELETE FROM transport_entries WHERE deleted = 0")

    conn.commit()
    conn.close()

# --- Permanently delete all soft-deleted entries (optional cleanup) ---
def purge_deleted_entries():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transport_entries WHERE deleted = 1")
    conn.commit()
    conn.close()