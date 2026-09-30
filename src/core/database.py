from __future__ import annotations

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / "data" / "pending_cases.db"

def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("""
      CREATE TABLE IF NOT EXISTS pending_cases(
        id INTEGER PRIMARY KEY,
        external_id TEXT NOT NULL UNIQUE,
        customer_name TEXT,
        phone TEXT,
        category TEXT,
        owner TEXT,
        status TEXT NOT NULL DEFAULT 'PENDING',
        notes TEXT,
        updated_at TEXT NOT NULL
      )
    """)
    conn.execute("""
      CREATE TABLE IF NOT EXISTS queue(
        id INTEGER PRIMARY KEY,
        case_id INTEGER NOT NULL REFERENCES pending_cases(id),
        channel TEXT NOT NULL,
        message TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'WAITING',
        created_at TEXT NOT NULL
      )
    """)
    return conn
