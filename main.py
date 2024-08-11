from loguru import logger
from rich.logging import RichHandler
from adaptive_llm_system import AdaptiveLLMSystem

# Set up pretty logging
logger.remove()
logger.add(RichHandler(), format="{message}", level="DEBUG")

if __name__ == "__main__":
    system = AdaptiveLLMSystem()

    previous_response = None
    while True:
        user_input = input("> ")
        if user_input.strip().lower() == "exit":
            break

        if previous_response:
            system.process_feedback(previous_response, user_input)

        response = system.process_input(user_input)
        print(f"System: {response}")
        previous_response = response

    system.shutdown()
