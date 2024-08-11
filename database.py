import sqlite3
from contextlib import contextmanager


class Database:
    def __init__(self, db_path="llm_system.db"):
        self.db_path = db_path
        self.init_db()

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()

    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Execute CREATE TABLE statements here
            conn.commit()
