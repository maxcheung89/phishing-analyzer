import sqlite3
from datetime import datetime

DB_PATH = "scan_results.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS scans (
                id TEXT PRIMARY KEY,
                target TEXT,
                log_file TEXT,
                pcap_file TEXT,
                vt_json TEXT,
                vt_link TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

def log_scan_result(scan_id, target, log_file, pcap_file, vt_json, vt_link):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO scans (id, target, log_file, pcap_file, vt_json, vt_link)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (scan_id, target, log_file, pcap_file or '', vt_json or '', vt_link or ''))

def get_history():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        return conn.execute("SELECT * FROM scans ORDER BY timestamp DESC").fetchall()
