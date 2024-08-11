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
from loguru import logger

class AdaptiveLLMSystem:
    def __init__(self):
        self.db = Database()
        self.task_label_tracker = TaskLabelTracker(self.db)
        self.model_manager = ModelManager(self.db)
        self.component_switcher = ComponentSwitcher(self.db)

        # Initialize other components
        self.expert_router = self.load_component("expert_router", ExpertRouter)
        self.prompt_optimizer = self.load_component("prompt_optimizer", BartPromptOptimizer)
        self.reasoning_model = self.load_component("reasoning_model", ReasoningModel, default_model="gpt2")

        self.dynamic_expert_creator = DynamicExpertCreator(self.model_manager)
        self.response_analyzer = ResponseAnalyzer()

    def load_component(self, component_name, component_class, default_model=None):
        model_name = self.component_switcher.get_current_model(component_name)
        if not model_name:
            model_name = self.model_manager.get_best_model_for_task(component_name)
            if not model_name:
                model_name = default_model or "gpt2"  # Use GPT-2 as a fallback
            self.component_switcher.switch_model(component_name, model_name)
        
        try:
            return component_class(model_name)
        except TypeError:
            # If the component doesn't accept a model_name, initialize it without arguments
            return component_class()

    def process_input(self, user_input):
        logger.debug(f"[Adaptive LLM System] Processing input: {user_input}")
        self.task_label_tracker.process_input(user_input)

        optimized_input = self.prompt_optimizer.optimize(user_input)
        logger.debug(f"[Adaptive LLM System] Optimized input: {optimized_input}")

        expert = self.expert_router.route(optimized_input)

        if not expert:
            logger.debug("[Adaptive LLM System] No expert found, creating new expert")
            expert_model = self.dynamic_expert_creator.create_expert(optimized_input)
            expert = self.reasoning_model

        llm_response = expert.generate(optimized_input)
        logger.debug(f"[Adaptive LLM System] Generated response: {llm_response}")
        return llm_response

    def process_feedback(self, llm_response, user_response):
        success_score = self.response_analyzer.analyze_response(llm_response, user_response)
        self.model_manager.update_model_performance(
            self.reasoning_model.name, "general", success_score
        )
        logger.debug(f"[Adaptive LLM System] Processed feedback. Success score: {success_score}")

    def shutdown(self):
        # Perform any necessary cleanup
        pass
