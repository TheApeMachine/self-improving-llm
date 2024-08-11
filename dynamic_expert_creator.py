from loguru import logger
from rich.logging import RichHandler

# Set up pretty logging
logger.remove()
logger.add(RichHandler(), format="{message}", level="DEBUG")

class DynamicExpertCreator:
    def __init__(self, model_manager):
        self.model_manager = model_manager
        logger.debug("[Dynamic Expert Creator] Initialized.")

    def create_expert(self, input_text):
        # For now, we'll just return a dummy expert
        # In the future, this method should analyze the input and create a specialized expert
        logger.debug(f"[Dynamic Expert Creator] Creating expert for input: {input_text}")
        
        # Get the best model for a general task
        model_name = self.model_manager.get_best_model_for_task("general")
        
        if not model_name:
            model_name = "default_model"  # Fallback to a default model
        
        # Here you would typically create and return a new expert
        # For now, we'll just return the model name
        logger.debug(f"[Dynamic Expert Creator] Created expert with model: {model_name}")
        return model_name

