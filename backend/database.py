import sqlite3

DB_PATH = "data/trust_data.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS datasets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT UNIQUE NOT NULL,
            file_hash TEXT NOT NULL,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def insert_dataset(filename: str, file_hash: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO datasets (filename, file_hash) VALUES (?, ?)",
        (filename, file_hash)
    )

    dataset_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return dataset_id


def get_dataset_by_filename(filename: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, file_hash FROM datasets WHERE filename = ?",
        (filename,)
    )

    row = cursor.fetchone()
    conn.close()
    return row  # (id, hash) or None


def get_hash_by_dataset_id(dataset_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT file_hash FROM datasets WHERE id = ?",
        (dataset_id,)
    )

    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None
