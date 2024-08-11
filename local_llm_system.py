from loguru import logger
from rich.logging import RichHandler

from bart_prompt_optimizer import BartPromptOptimizer
from expert_router import ExpertRouter
from memory_system import MemorySystem
from prompt_analyzer import PromptAnalyzer
from reasoning_model import ReasoningModel

# Set up pretty logging
logger.remove()
logger.add(RichHandler(), format="{message}", level="DEBUG")


# Main system that ties everything together
class LocalLLMSystem:
    def __init__(self):
        self.analyzer = PromptAnalyzer()
        self.optimizer = BartPromptOptimizer()
        self.expert_router = ExpertRouter()
        self.memory = MemorySystem()

        # Register various experts
        reasoning_model = ReasoningModel(
            "EleutherAI/gpt-neo-1.3B"
        )  # Replace with more suitable models as needed
        strategy_model = ReasoningModel(
            "EleutherAI/gpt-neo-1.3B"
        )  # Use a different model for strategy generation
        general_model = ReasoningModel("EleutherAI/gpt-neo-1.3B")

        self.expert_router.register_expert("reasoning_model", reasoning_model)
        self.expert_router.register_expert("strategy_generation_model", strategy_model)
        self.expert_router.register_expert("general", general_model)

    def process_prompt(self, prompt: str):
        logger.info(f"[System] Processing prompt: {prompt}")

        # Check memory for past relevant interactions
        past_interactions = self.memory.retrieve_past_interactions(prompt)
        if past_interactions:
            logger.info(
                "[System] Found relevant past interactions, retrieving responses."
            )
            return past_interactions

        # Analyze and optimize the prompt
        intent, raw_prompt = self.analyzer.analyze(prompt)
        optimized_prompt = self.optimizer.optimize(raw_prompt)

        # Route the optimized prompt to the appropriate experts
        responses = self.expert_router.route(intent, optimized_prompt)

        # Store the interaction in memory
        final_response = " ".join(responses)
        self.memory.store_interaction(prompt, final_response)
        return final_response

    def close(self):
        pass
