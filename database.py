import sqlite3

from datetime import datetime
from vars import DATABASE


def get_connection():
    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    return conn


def setup_database():
    """Sets up the SQLite database with tables for URLs and access logs."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS urls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        original_url TEXT NOT NULL,
        short_url TEXT NOT NULL UNIQUE,
        created_at INTEGER NOT NULL,
        expires_at INTEGER NOT NULL,
        password TEXT
    )
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS access_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        short_url TEXT NOT NULL,
        accessed_at INTEGER NOT NULL,
        ip_address TEXT NOT NULL,
        FOREIGN KEY (short_url) REFERENCES urls (short_url) ON DELETE CASCADE
    )
    """
    )

    conn.commit()
    conn.close()


def insert_url(original_url, short_url, expires_at, password=None):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
        INSERT INTO urls (original_url, short_url, created_at, expires_at, password)
        VALUES (?, ?, ?, ?, ?)
        """,
            (original_url, short_url, datetime.now(), expires_at, password),
        )

        conn.commit()


def get_url(url, type="short"):
    with get_connection() as conn:
        cursor = conn.cursor()

        if type == "short":
            cursor.execute("SELECT * FROM urls WHERE short_url = ?", (url,))
        else:
            cursor.execute("SELECT * FROM urls WHERE original_url = ?", (url,))

        return cursor.fetchone()


def log_access(short_url, ip_address):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
        INSERT INTO access_logs (short_url, accessed_at, ip_address)
        VALUES (?, ?, ?)
        """,
            (short_url, datetime.now(), ip_address),
        )

        conn.commit()


def get_analytics(short_url):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
        SELECT accessed_at, ip_address FROM access_logs WHERE short_url = ?
        """,
            (short_url,),
        )

        return cursor.fetchall()
