class TaskLabelTracker:
    def __init__(self, db):
        self.db = db

    def process_input(self, user_input):
        labels = self.label_classifier(user_input)
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            for label in labels:
                cursor.execute(
                    """
                    INSERT INTO task_labels (label, count)
                    VALUES (?, 1)
                    ON CONFLICT(label) DO UPDATE SET count = count + 1
                """,
                    (label,),
                )
            conn.commit()

    def get_top_labels(self, n=5):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT label, count FROM task_labels ORDER BY count DESC LIMIT ?", (n,)
            )
            return cursor.fetchall()
