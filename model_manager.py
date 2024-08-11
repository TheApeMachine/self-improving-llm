class ModelManager:
    def __init__(self, db):
        self.db = db

    def add_model(self, name, model_type):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR IGNORE INTO models (name, type) VALUES (?, ?)",
                (name, model_type),
            )
            conn.commit()

    def update_model_performance(self, model_name, task, score):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE models SET performance_score = ? WHERE name = ?",
                (score, model_name),
            )
            cursor.execute(
                """
                INSERT INTO performance_history (model_id, task, score)
                VALUES ((SELECT id FROM models WHERE name = ?), ?, ?)
            """,
                (model_name, task, score),
            )
            conn.commit()

    def get_best_model_for_task(self, task):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT m.name
                FROM models m
                JOIN performance_history ph ON m.id = ph.model_id
                WHERE ph.task = ?
                ORDER BY ph.score DESC
                LIMIT 1
            """,
                (task,),
            )
            result = cursor.fetchone()
            return result[0] if result else None
