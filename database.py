# database.py
import sqlite3
from contextlib import contextmanager


class Database:
    def __init__(self, db_path="llm_system.db"):
        self.db_path = db_path
        self.init_db()

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # This allows accessing columns by name
        try:
            yield conn
        finally:
            conn.close()

    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Execute CREATE TABLE statements here
            cursor.executescript(
                """
                CREATE TABLE IF NOT EXISTS task_labels (
                    id INTEGER PRIMARY KEY,
                    label TEXT UNIQUE NOT NULL,
                    count INTEGER DEFAULT 0
                );

                CREATE TABLE IF NOT EXISTS models (
                    id INTEGER PRIMARY KEY,
                    name TEXT UNIQUE NOT NULL,
                    type TEXT NOT NULL,
                    performance_score REAL
                );

                CREATE TABLE IF NOT EXISTS component_model_assignments (
                    id INTEGER PRIMARY KEY,
                    component_name TEXT NOT NULL,
                    model_id INTEGER,
                    FOREIGN KEY (model_id) REFERENCES models(id)
                );

                CREATE TABLE IF NOT EXISTS performance_history (
                    id INTEGER PRIMARY KEY,
                    model_id INTEGER,
                    task TEXT NOT NULL,
                    score REAL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (model_id) REFERENCES models(id)
                );
            """
            )
            conn.commit()
