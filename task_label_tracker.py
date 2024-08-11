from database import Database
from loguru import logger
from rich.logging import RichHandler
from transformers import pipeline

# Set up pretty logging
logger.remove()
logger.add(RichHandler(), format="{message}", level="DEBUG")

class TaskLabelTracker:
    def __init__(self, db: Database):
        self.db = db
        self.label_classifier = self.load_label_classifier()
        logger.debug("[Task Label Tracker] Initialized.")

    def load_label_classifier(self):
        # Use a pre-trained zero-shot classification model
        classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
        logger.debug("[Task Label Tracker] Loaded zero-shot classification model.")
        return classifier

    def process_input(self, user_input):
        # Define a set of possible labels
        candidate_labels = ["news", "weather", "sports", "technology", "entertainment", "general"]
        
        # Classify the input
        result = self.label_classifier(user_input, candidate_labels)
        labels = [label for label, score in zip(result['labels'], result['scores']) if score > 0.3]
        
        if not labels:
            labels = ["general"]
        
        logger.debug(f"[Task Label Tracker] Classified input: {user_input} as {labels}")
        
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
