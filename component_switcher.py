# component_switcher.py
from database import Database


class ComponentSwitcher:
    def __init__(self, db: Database):
        self.db = db

    def switch_model(self, component, model_name):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO component_model_assignments (component_name, model_id)
                VALUES (?, (SELECT id FROM models WHERE name = ?))
            """,
                (component, model_name),
            )
            conn.commit()

    def get_current_model(self, component):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT m.name
                FROM component_model_assignments cma
                JOIN models m ON cma.model_id = m.id
                WHERE cma.component_name = ?
            """,
                (component,),
            )
            result = cursor.fetchone()
            return result["name"] if result else None
