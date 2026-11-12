import sqlite3
import logging
from datetime import datetime, date
from typing import Optional, List, Dict, Any
from config import DATABASE_PATH, SUPABASE_URL, SUPABASE_KEY

logger = logging.getLogger(__name__)

# Initialize Supabase client if configured
supabase_client = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        from supabase import create_client, Client
        supabase_client: Optional[Client] = create_client(SUPABASE_URL, SUPABASE_KEY)
        logger.info("Supabase cloud client initialized successfully.")
    except Exception as e:
        logger.warning(f"Could not initialize Supabase client: {e}")

def get_supabase():
    global supabase_client
    if supabase_client is None and SUPABASE_URL and SUPABASE_KEY:
        try:
            from supabase import create_client
            supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
        except Exception as e:
            logger.warning(f"Failed to create Supabase client on demand: {e}")
    return supabase_client

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

    # Spaced Repetition System (SRS) table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS srs_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            item_type TEXT DEFAULT 'vocab',
            prompt TEXT NOT NULL,
            correct_answer TEXT NOT NULL,
            options_json TEXT NOT NULL,
            explanation TEXT,
            interval_stage INTEGER DEFAULT 1,
            next_review_date TEXT,
            review_count INTEGER DEFAULT 0,
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

    try:
        cursor.execute("ALTER TABLE users ADD COLUMN scenario_state TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute("ALTER TABLE users ADD COLUMN fluency_score INTEGER DEFAULT 75")
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

    # Cloud sync to Supabase
    sb = get_supabase()
    if sb:
        try:
            sb.table("users").upsert({
                "user_id": user_id,
                "chat_id": chat_id,
                "username": username,
                "first_name": first_name,
                "streak": user_dict.get("streak", 1),
                "last_active_date": user_dict.get("last_active_date", today_str),
                "level": user_dict.get("level", "Intermediate"),
                "mode": user_dict.get("mode", "Native"),
                "accent": user_dict.get("accent", "US"),
                "voice_enabled": user_dict.get("voice_enabled", 1),
                "interview_state": user_dict.get("interview_state", "")
            }).execute()
        except Exception as e:
            logger.debug(f"Supabase upsert user error: {e}")

    return user_dict

def update_user_level(user_id: int, level: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET level = ? WHERE user_id = ?", (level, user_id))
    conn.commit()
    conn.close()
    sb = get_supabase()
    if sb:
        try:
            sb.table("users").update({"level": level}).eq("user_id", user_id).execute()
        except Exception as e:
            logger.debug(f"Supabase update_user_level error: {e}")

def update_user_voice(user_id: int, enabled: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET voice_enabled = ? WHERE user_id = ?", (enabled, user_id))
    conn.commit()
    conn.close()
    sb = get_supabase()
    if sb:
        try:
            sb.table("users").update({"voice_enabled": enabled}).eq("user_id", user_id).execute()
        except Exception as e:
            logger.debug(f"Supabase update_user_voice error: {e}")

def update_user_accent(user_id: int, accent: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET accent = ? WHERE user_id = ?", (accent, user_id))
    conn.commit()
    conn.close()
    sb = get_supabase()
    if sb:
        try:
            sb.table("users").update({"accent": accent}).eq("user_id", user_id).execute()
        except Exception as e:
            logger.debug(f"Supabase update_user_accent error: {e}")

def set_interview_state(user_id: int, state: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET interview_state = ? WHERE user_id = ?", (state, user_id))
    conn.commit()
    conn.close()
    sb = get_supabase()
    if sb:
        try:
            sb.table("users").update({"interview_state": state}).eq("user_id", user_id).execute()
        except Exception as e:
            logger.debug(f"Supabase set_interview_state error: {e}")

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

    sb = get_supabase()
    if sb:
        try:
            sb.table("chat_history").insert({"user_id": user_id, "role": role, "content": content}).execute()
        except Exception as e:
            logger.debug(f"Supabase add_chat_history error: {e}")

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
    sb = get_supabase()
    if sb:
        try:
            sb.table("chat_history").delete().eq("user_id", user_id).execute()
        except Exception as e:
            logger.debug(f"Supabase clear_chat_history error: {e}")

def save_vocabulary(user_id: int, word: str, meaning_bn: str, part_of_speech: str = "", example_sentence: str = ""):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO vocabulary (user_id, word, meaning_bn, part_of_speech, example_sentence)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, word, meaning_bn, part_of_speech, example_sentence))
    conn.commit()
    conn.close()

    sb = get_supabase()
    if sb:
        try:
            sb.table("vocabulary").insert({
                "user_id": user_id,
                "word": word,
                "meaning_bn": meaning_bn,
                "part_of_speech": part_of_speech,
                "example_sentence": example_sentence
            }).execute()
        except Exception as e:
            logger.debug(f"Supabase save_vocabulary error: {e}")

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

    sb = get_supabase()
    if sb:
        try:
            sb.table("mistakes_log").insert({
                "user_id": user_id,
                "original_text": original,
                "corrected_text": corrected,
                "explanation": explanation
            }).execute()
        except Exception as e:
            logger.debug(f"Supabase save_mistake error: {e}")

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

def sync_sqlite_to_supabase() -> Dict[str, int]:
    """One-click batch sync from local SQLite database to Supabase Cloud."""
    sb = get_supabase()
    if not sb:
        return {"error": "Supabase client not configured or key missing"}
    
    conn = get_connection()
    cursor = conn.cursor()
    stats = {"users": 0, "vocabulary": 0, "mistakes": 0}

    # 1. Users
    cursor.execute("SELECT * FROM users")
    users = [dict(r) for r in cursor.fetchall()]
    for u in users:
        try:
            sb.table("users").upsert(u).execute()
            stats["users"] += 1
        except Exception as e:
            logger.debug(f"User sync error: {e}")

    # 2. Vocabulary
    cursor.execute("SELECT user_id, word, meaning_bn, part_of_speech, example_sentence FROM vocabulary")
    vocabs = [dict(r) for r in cursor.fetchall()]
    for v in vocabs:
        try:
            sb.table("vocabulary").insert(v).execute()
            stats["vocabulary"] += 1
        except Exception as e:
            logger.debug(f"Vocab sync error: {e}")

    # 3. Mistakes
    cursor.execute("SELECT user_id, original_text, corrected_text, explanation FROM mistakes_log")
    mistakes = [dict(r) for r in cursor.fetchall()]
    for m in mistakes:
        try:
            sb.table("mistakes_log").insert(m).execute()
            stats["mistakes"] += 1
        except Exception as e:
            logger.debug(f"Mistake sync error: {e}")

    conn.close()
    return stats

def set_scenario_state(user_id: int, state: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET scenario_state = ? WHERE user_id = ?", (state, user_id))
    conn.commit()
    conn.close()

def get_scenario_state(user_id: int) -> str:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT scenario_state FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row["scenario_state"] if row and row["scenario_state"] else ""

def add_srs_item(user_id: int, prompt: str, correct_answer: str, options: List[str], explanation: str = "", item_type: str = "vocab"):
    import json
    from datetime import date, timedelta
    conn = get_connection()
    cursor = conn.cursor()
    # Next review tomorrow by default (1 day interval)
    next_date = (date.today() + timedelta(days=1)).isoformat()
    cursor.execute("""
        INSERT INTO srs_items (user_id, item_type, prompt, correct_answer, options_json, explanation, interval_stage, next_review_date)
        VALUES (?, ?, ?, ?, ?, ?, 1, ?)
    """, (user_id, item_type, prompt, correct_answer, json.dumps(options), explanation, next_date))
    conn.commit()
    conn.close()

def get_due_srs_items(user_id: int, limit: int = 3) -> List[Dict[str, Any]]:
    import json
    from datetime import date
    conn = get_connection()
    cursor = conn.cursor()
    today_str = date.today().isoformat()
    cursor.execute("""
        SELECT * FROM srs_items 
        WHERE user_id = ? AND (next_review_date <= ? OR next_review_date IS NULL)
        ORDER BY interval_stage ASC, id ASC
        LIMIT ?
    """, (user_id, today_str, limit))
    rows = cursor.fetchall()
    results = []
    for r in rows:
        d = dict(r)
        try:
            d["options"] = json.loads(d["options_json"])
        except Exception:
            d["options"] = []
        results.append(d)
    conn.close()
    return results

def update_srs_item_result(item_id: int, is_correct: bool):
    from datetime import date, timedelta
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT interval_stage, review_count FROM srs_items WHERE id = ?", (item_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return

    current_stage = row["interval_stage"]
    review_count = row["review_count"] + 1

    if is_correct:
        # Progress stages: 1 day -> 3 days -> 7 days -> 21 days
        new_stage = min(current_stage + 1, 4)
        intervals = {1: 1, 2: 3, 3: 7, 4: 21}
        days_to_add = intervals.get(new_stage, 7)
    else:
        # Reset on failure
        new_stage = 1
        days_to_add = 1

    next_review = (date.today() + timedelta(days=days_to_add)).isoformat()
    cursor.execute("""
        UPDATE srs_items 
        SET interval_stage = ?, next_review_date = ?, review_count = ?
        WHERE id = ?
    """, (new_stage, next_review, review_count, item_id))
    conn.commit()
    conn.close()

def get_user_learning_metrics(user_id: int) -> Dict[str, Any]:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    user_dict = dict(user) if user else {}

    cursor.execute("SELECT COUNT(*) FROM vocabulary WHERE user_id = ?", (user_id,))
    vocab_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM mistakes_log WHERE user_id = ?", (user_id,))
    mistakes_count = cursor.fetchone()[0]

    cursor.execute("SELECT word, meaning_bn, example_sentence, learned_at FROM vocabulary WHERE user_id = ? ORDER BY id DESC LIMIT 15", (user_id,))
    recent_vocabs = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT original_text, corrected_text, explanation FROM mistakes_log WHERE user_id = ? ORDER BY id DESC LIMIT 10", (user_id,))
    recent_mistakes = [dict(r) for r in cursor.fetchall()]

    # Calculate dynamic fluency score
    streak = user_dict.get("streak", 1)
    base_score = 65
    score = min(99, base_score + (streak * 2) + min(vocab_count, 15) - min(mistakes_count // 3, 5))

    conn.close()
    return {
        "user": user_dict,
        "vocab_count": vocab_count,
        "mistakes_count": mistakes_count,
        "fluency_score": score,
        "recent_vocabs": recent_vocabs,
        "recent_mistakes": recent_mistakes
    }
