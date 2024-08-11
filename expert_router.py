from loguru import logger
from rich.logging import RichHandler

# Set up pretty logging
logger.remove()
logger.add(RichHandler(), format="{message}", level="DEBUG")

class ExpertRouter:
    def __init__(self, model_name=None):
        self.model_name = model_name
        self.experts = {}
        logger.debug(f"[Expert Router] Initialized with model: {model_name}")

    def register_expert(self, expert_name, expert):
        self.experts[expert_name] = expert
        logger.debug(f"[Expert Router] Registered expert: {expert_name}")

    def route(self, optimized_prompt):
        # For now, we'll just return a dummy expert
        # In the future, this method should analyze the prompt and route to the appropriate expert
        logger.debug(f"[Expert Router] Routing prompt: {optimized_prompt}")
        
        if self.experts:
            expert_name = next(iter(self.experts))
            logger.debug(f"[Expert Router] Routed to expert: {expert_name}")
            return self.experts[expert_name]
        else:
            logger.debug("[Expert Router] No experts available, returning None")
            return None
