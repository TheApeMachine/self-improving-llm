from loguru import logger
from rich.logging import RichHandler

# Set up pretty logging
logger.remove()
logger.add(RichHandler(), format="{message}", level="DEBUG")

from local_llm_system import LocalLLMSystem

if __name__ == "__main__":
    system = LocalLLMSystem()

    while True:
        prompt = input("> ")
        if prompt.strip() == "exit":
            break

        response = system.process_prompt(prompt)
        logger.info(f"[System] Final Response: {response}")

    system.close()
