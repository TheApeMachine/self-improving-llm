from transformers import pipeline

from loguru import logger
from rich.logging import RichHandler

# Set up pretty logging
logger.remove()
logger.add(RichHandler(), format="{message}", level="DEBUG")


# Prompt analyzer using zero-shot classification
class PromptAnalyzer:
    def __init__(self):
        self.intent_classifier = pipeline(
            "zero-shot-classification", model="facebook/bart-large-mnli"
        )
        logger.debug("[Prompt Analyzer] Initialized zero-shot classification model.")

    def analyze(self, prompt: str):
        logger.debug(f"[Prompt Analyzer] Analyzing prompt: {prompt}")
        candidate_labels = [
            "analysis",
            "strategy",
            "information retrieval",
            "recommendation",
            "other",
        ]
        result = self.intent_classifier(prompt, candidate_labels)
        top_intent = result["labels"][0]  # Get the top predicted intent
        logger.debug(f"[Prompt Analyzer] Detected intent: {top_intent}")
        return top_intent, prompt
