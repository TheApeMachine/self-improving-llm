from loguru import logger
from rich.logging import RichHandler
from transformers import AutoModelForCausalLM, AutoTokenizer

from base_model import BaseModel

# Set up pretty logging
logger.remove()
logger.add(RichHandler(), format="{message}", level="DEBUG")


class ReasoningModel(BaseModel):
    def __init__(self, model_name: str):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        logger.debug(f"[Reasoning Model] Initialized with model {model_name}.")

    def generate(self, prompt: str, max_new_tokens: int = 150) -> str:
        logger.debug(f"[Reasoning Model] Generating response for prompt: {prompt}")
        inputs = self.tokenizer(
            prompt, return_tensors="pt", truncation=True, max_length=1024
        )
        outputs = self.model.generate(**inputs, max_new_tokens=max_new_tokens)
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        logger.debug(f"[Reasoning Model] Generated response: {response}")
        return response
