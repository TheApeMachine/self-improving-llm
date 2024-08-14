from .expert_manager import ExpertManager

class TaskRouter:
    def __init__(self):
        self.expert_manager = ExpertManager()

    def route_task(self, task):
        # Example logic to select the appropriate expert based on the task
        expert = self.expert_manager.get_expert("ExampleExpert")
        if expert:
            return expert.process(task)
        else:
            return f"No expert found for task '{task}'"
