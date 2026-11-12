import sqlite3
from datetime import datetime, date
from typing import Optional, List, Dict, Any
from config import DATABASE_PATH

def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            chat_id INTEGER UNIQUE NOT NULL,
            username TEXT,
            first_name TEXT,
            level TEXT DEFAULT 'Intermediate', -- Beginner, Intermediate, Advanced
            mode TEXT DEFAULT 'Tutor',        -- Tutor (chat+correction), Strict (grammar only), Conversational, Business
            streak INTEGER DEFAULT 1,
            last_active_date TEXT,
            daily_reminder_time TEXT DEFAULT '09:00',
            notifications_enabled INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Conversation history table (for short-term memory)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            role TEXT, -- 'user' or 'model'
            content TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    """)

    # Vocabulary bank
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vocabulary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            word TEXT NOT NULL,
            meaning_bn TEXT,
            part_of_speech TEXT,
            example_sentence TEXT,
            learned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    """)

    # Mistakes & corrections log
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mistakes_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            original_text TEXT,
            corrected_text TEXT,
            explanation TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    """)

    # Safe migrations for new features
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN voice_enabled INTEGER DEFAULT 1")
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute("ALTER TABLE users ADD COLUMN accent TEXT DEFAULT 'US'")
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute("ALTER TABLE users ADD COLUMN interview_state TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass

    conn.commit()
    conn.close()

def get_or_create_user(user_id: int, chat_id: int, username: str = "", first_name: str = "") -> Dict[str, Any]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()

    today_str = date.today().isoformat()

    if not row:
        cursor.execute("""
            INSERT INTO users (user_id, chat_id, username, first_name, streak, last_active_date)
            VALUES (?, ?, ?, ?, 1, ?)
        """, (user_id, chat_id, username, first_name, today_str))
        conn.commit()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
    else:
        # Check streak
        last_date_str = row["last_active_date"]
        streak = row["streak"]
        if last_date_str != today_str:
            if last_date_str:
                last_date = date.fromisoformat(last_date_str)
                delta_days = (date.today() - last_date).days
                if delta_days == 1:
                    streak += 1
                elif delta_days > 1:
                    streak = 1
            cursor.execute("""
                UPDATE users SET last_active_date = ?, streak = ?, chat_id = ?
                WHERE user_id = ?
            """, (today_str, streak, chat_id, user_id))
            conn.commit()

    user_dict = dict(row)
    conn.close()
    return user_dict

def update_user_level(user_id: int, level: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET level = ? WHERE user_id = ?", (level, user_id))
    conn.commit()
    conn.close()

def update_user_voice(user_id: int, enabled: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET voice_enabled = ? WHERE user_id = ?", (enabled, user_id))
    conn.commit()
    conn.close()

def update_user_accent(user_id: int, accent: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET accent = ? WHERE user_id = ?", (accent, user_id))
    conn.commit()
    conn.close()

def set_interview_state(user_id: int, state: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET interview_state = ? WHERE user_id = ?", (state, user_id))
    conn.commit()
    conn.close()

def get_interview_state(user_id: int) -> str:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT interview_state FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row["interview_state"] if row and row["interview_state"] else ""

def get_recent_mistakes(user_id: int, limit: int = 5) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT original_text, corrected_text, explanation, created_at 
        FROM mistakes_log 
        WHERE user_id = ? 
        ORDER BY id DESC LIMIT ?
    """, (user_id, limit))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def update_user_mode(user_id: int, mode: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET mode = ? WHERE user_id = ?", (mode, user_id))
    conn.commit()
    conn.close()

def add_chat_history(user_id: int, role: str, content: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chat_history (user_id, role, content) VALUES (?, ?, ?)", (user_id, role, content))
    conn.commit()
    # Keep only last 20 messages per user to maintain context without overloading
    cursor.execute("""
        DELETE FROM chat_history
        WHERE id NOT IN (
            SELECT id FROM chat_history WHERE user_id = ? ORDER BY id DESC LIMIT 20
        ) AND user_id = ?
    """, (user_id, user_id))
    conn.commit()
    conn.close()

def get_chat_history(user_id: int, limit: int = 8) -> List[Dict[str, str]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT role, content FROM chat_history WHERE user_id = ? ORDER BY id ASC LIMIT ?", (user_id, limit))
    rows = cursor.fetchall()
    conn.close()
    return [{"role": r["role"], "content": r["content"]} for r in rows]

def clear_chat_history(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chat_history WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

def save_vocabulary(user_id: int, word: str, meaning_bn: str, part_of_speech: str = "", example_sentence: str = ""):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO vocabulary (user_id, word, meaning_bn, part_of_speech, example_sentence)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, word, meaning_bn, part_of_speech, example_sentence))
    conn.commit()
    conn.close()

def get_user_vocab_count(user_id: int) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM vocabulary WHERE user_id = ?", (user_id,))
    count = cursor.fetchone()[0]
    conn.close()
    return count

def save_mistake(user_id: int, original: str, corrected: str, explanation: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO mistakes_log (user_id, original_text, corrected_text, explanation)
        VALUES (?, ?, ?, ?)
    """, (user_id, original, corrected, explanation))
    conn.commit()
    conn.close()

def get_user_mistakes_count(user_id: int) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM mistakes_log WHERE user_id = ?", (user_id,))
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_all_subscribers() -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, chat_id, first_name, level, mode, streak FROM users WHERE notifications_enabled = 1")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]
