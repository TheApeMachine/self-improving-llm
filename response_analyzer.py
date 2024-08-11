from loguru import logger
from rich.logging import RichHandler
from transformers import pipeline

# Set up pretty logging
logger.remove()
logger.add(RichHandler(), format="{message}", level="DEBUG")

class ResponseAnalyzer:
    def __init__(self):
        self.sentiment_analyzer = pipeline("sentiment-analysis")
        logger.debug("[Response Analyzer] Initialized with sentiment analyzer.")

    def analyze_response(self, llm_response, user_response):
        # Check if the user response contains feedback indicators
        feedback_indicators = ["good", "great", "excellent", "bad", "poor", "incorrect", "wrong"]
        contains_feedback = any(indicator in user_response.lower() for indicator in feedback_indicators)

        # Perform sentiment analysis
        sentiment_result = self.sentiment_analyzer(user_response)[0]
        sentiment_score = sentiment_result['score'] if sentiment_result['label'] == 'POSITIVE' else -sentiment_result['score']

        # Determine the final score
        if contains_feedback:
            score = (sentiment_score + 1) / 2  # Normalize to 0-1 range
        else:
            score = 0.5  # Neutral score if no clear feedback

        logger.debug(f"[Response Analyzer] Analyzed response. Contains feedback: {contains_feedback}, Sentiment: {sentiment_score}, Final score: {score}")
        return score
