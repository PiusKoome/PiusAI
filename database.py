import sqlite3

DB_NAME = "pius_ai.db"

def init_db():
    """Create the SQLite database and table if they don't exist yet."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_message(role, content):
    """Save a single message (user or assistant) into the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO chat_history (role, content)
        VALUES (?, ?)
    ''', (role, content))
    conn.commit()
    conn.close()

def load_chat_history(limit=20):
    """Retrieve recent chat history formatted for your AI API payload."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Grab the last N messages ordered chronologically
    cursor.execute('''
        SELECT role, content FROM (
            SELECT id, role, content FROM chat_history
            ORDER BY id DESC
            LIMIT ?
        ) ORDER BY id ASC
    ''', (limit,))
    
    rows = cursor.fetchall()
    conn.close()
    
    # Return formatted list of dicts: [{'role': 'user', 'content': '...'}, ...]
    return [{"role": row[0], "content": row[1]} for row in rows]