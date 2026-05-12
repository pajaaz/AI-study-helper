import sqlite3

DB_NAME = "study_helper.db"

def init_db():
    """Vytvoří tabulku, pokud ještě neexistuje."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_text TEXT,
            summary TEXT,
            questions TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_to_db(original_text, summary, questions):
    """Uloží nový záznam do databáze."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO history (original_text, summary, questions)
        VALUES (?, ?, ?)
    ''', (original_text, summary, questions))
    conn.commit()
    conn.close()

def get_history():
    """Načte historii z databáze od nejnovějšího."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, summary, questions, created_at FROM history ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows