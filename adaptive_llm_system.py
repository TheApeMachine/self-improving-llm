# adaptive_llm_system.py
from dynamic_expert_creator import DynamicExpertCreator
from response_analyzer import ResponseAnalyzer

from bart_prompt_optimizer import BartPromptOptimizer
from component_switcher import ComponentSwitcher
from database import Database
from expert_router import ExpertRouter
from model_manager import ModelManager
from reasoning_model import ReasoningModel
from task_label_tracker import TaskLabelTracker


class AdaptiveLLMSystem:
    def __init__(self):
        self.db = Database()
        self.task_label_tracker = TaskLabelTracker(self.db)
        self.model_manager = ModelManager(self.db)
        self.component_switcher = ComponentSwitcher(self.db)

        # Initialize other components
        self.expert_router = self.load_component("expert_router", ExpertRouter)
        self.prompt_optimizer = self.load_component(
            "prompt_optimizer", BartPromptOptimizer
        )
        self.reasoning_model = self.load_component("reasoning_model", ReasoningModel)

        self.dynamic_expert_creator = DynamicExpertCreator(self.model_manager)
        self.response_analyzer = ResponseAnalyzer()

    def load_component(self, component_name, component_class):
        model_name = self.component_switcher.get_current_model(component_name)
        if not model_name:
            model_name = self.model_manager.get_best_model_for_task(component_name)
            if not model_name:
                model_name = "default_model"  # Fallback to default
            self.component_switcher.switch_model(component_name, model_name)
        return component_class(model_name)

    def process_input(self, user_input):
        self.task_label_tracker.process_input(user_input)

        optimized_input = self.prompt_optimizer.optimize(user_input)
        expert = self.expert_router.route(optimized_input)

        if not expert:
            expert = self.dynamic_expert_creator.create_expert(optimized_input)

        llm_response = expert.generate_response(optimized_input)
        return llm_response

    def process_feedback(self, llm_response, human_response):
        success_score = self.response_analyzer.analyze_response(
            llm_response, human_response
        )
        self.model_manager.update_model_performance(
            self.reasoning_model.name, "general", success_score
        )

    def run(self):
        while True:
            user_input = input("Enter your query: ")
            llm_response = self.process_input(user_input)
            print(llm_response)

            human_response = input("Your feedback: ")
            self.process_feedback(llm_response, human_response)

    def shutdown(self):
        # Perform any necessary cleanup
        pass
