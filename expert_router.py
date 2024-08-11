# expert_router.py

from bs4 import BeautifulSoup
from loguru import logger

from headless_browser import HeadlessBrowser
from reasoning_model import BaseModel


class ExpertRouter:
    def __init__(self):
        self.experts = {}
        self.browser = HeadlessBrowser()
        logger.debug("[Expert Router] Initialized expert router.")

    def register_expert(self, model_name: str, expert: BaseModel):
        self.experts[model_name] = expert
        logger.debug(f"[Expert Router] Registered expert model: {model_name}.")

    def route(self, intent: str, optimized_prompt: str):
        logger.debug(f"[Expert Router] Routing based on intent: {intent}")
        selected_experts = []

        # Check if the prompt requires real-time data from the web
        if (
            "latest news" in optimized_prompt.lower()
            or "current events" in optimized_prompt.lower()
        ):
            url = "https://news.ycombinator.com/"  # You can change this URL to another news site
            page_content = self.browser.fetch_data(url)

            # Use BeautifulSoup to parse and truncate the content
            soup = BeautifulSoup(page_content, "html.parser")
            text_content = soup.get_text(separator=" ", strip=True)
            truncated_content = text_content[
                :2000
            ]  # Truncate to 2000 characters (adjust as needed)

            optimized_prompt += " " + truncated_content
            logger.debug(
                f"[Expert Router] Appended real-time data to prompt: {optimized_prompt}"
            )

        # Select experts based on the intent or optimized prompt analysis
        if "analysis" in optimized_prompt.lower():
            selected_experts.append("reasoning_model")
        elif (
            "strategy" in optimized_prompt.lower() or "plan" in optimized_prompt.lower()
        ):
            selected_experts.append("strategy_generation_model")
        else:
            selected_experts.append("general")

        # Collect responses from selected experts
        responses = []
        for expert_name in selected_experts:
            expert = self.experts.get(expert_name)
            if expert:
                responses.append(expert.generate(optimized_prompt, max_new_tokens=150))

        return responses
