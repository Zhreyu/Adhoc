import sqlite3
import os

DB_PATH = '.Adhoc/adhoc.db'

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn

def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS changes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path TEXT NOT NULL,
            change_type TEXT NOT NULL,
            old_code TEXT,
            new_code TEXT,
            explanation TEXT,
            user_message TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            summary TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS explanations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path TEXT,
            explanation TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS codebase_summary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            summary TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_codebase_summary(summary):
    """Save the codebase summary to the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO codebase_summary (summary) VALUES (?)', (summary,))
    conn.commit()
    conn.close()

def get_codebase_summary():
    """Retrieve the latest codebase summary from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT summary FROM codebase_summary ORDER BY id DESC LIMIT 1')
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def save_explanations(explanations):
    """
    Save a list of explanations to the database.
    Each explanation is a dictionary with 'file_path' and 'explanation' keys.
    """
    conn = get_connection()
    cursor = conn.cursor()
    for item in explanations:
        cursor.execute('''
            INSERT INTO explanations (file_path, explanation)
            VALUES (?, ?)
        ''', (item['file_path'], item['explanation']))
    conn.commit()
    conn.close()

def get_explanations():
    """
    Retrieve all explanations from the database.
    Returns a list of dictionaries with 'file_path', 'explanation', and 'timestamp'.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT file_path, explanation, timestamp FROM explanations ORDER BY timestamp')
    rows = cursor.fetchall()
    conn.close()
    explanations = []
    for row in rows:
        explanations.append({
            'file_path': row[0],
            'explanation': row[1],
            'timestamp': row[2]
        })
    return explanations
