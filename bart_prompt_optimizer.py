from transformers import (
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
)

from loguru import logger
from rich.logging import RichHandler

# Set up pretty logging
logger.remove()
logger.add(RichHandler(), format="{message}", level="DEBUG")


# BART-based prompt optimizer
class BartPromptOptimizer:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
        self.model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")
        logger.debug("[Prompt Optimizer] Initialized BART prompt optimizer.")

    def optimize(self, prompt: str) -> str:
        logger.debug(f"[Prompt Optimizer] Optimizing prompt: {prompt}")
        inputs = self.tokenizer(
            prompt, return_tensors="pt", max_length=1024, truncation=True
        )
        summary_ids = self.model.generate(
            inputs["input_ids"],
            max_length=150,
            min_length=40,
            length_penalty=2.0,
            num_beams=4,
            early_stopping=True,
        )
        optimized_prompt = self.tokenizer.decode(
            summary_ids[0], skip_special_tokens=True
        )
        logger.debug(f"[Prompt Optimizer] Optimized prompt: {optimized_prompt}")
        return optimized_prompt
