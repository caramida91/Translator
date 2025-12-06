import sqlite3
import bcrypt

class DatabaseManager:
    def __init__(self, db_name="users.db"):
        self.db_name = db_name
        self.create_users_table()

    def connect(self):
        return sqlite3.connect(self.db_name)

    def create_users_table(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def register_user(self, username, password):
        conn = self.connect()
        cursor = conn.cursor()

        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        try:
            cursor.execute(
                "INSERT INTO users(username, password_hash) VALUES(?, ?)",
                (username, hashed)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def login_user(self, username, password):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return False

        return bcrypt.checkpw(password.encode(), row[0])
