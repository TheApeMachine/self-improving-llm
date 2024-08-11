import asyncio
from loguru import logger
from rich.logging import RichHandler
from adaptive_llm_system import AdaptiveLLMSystem

# Set up pretty logging
logger.remove()
logger.add(RichHandler(), format="{message}", level="DEBUG")

async def main():
    try:
        system = AdaptiveLLMSystem()
        logger.info("AdaptiveLLMSystem initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize AdaptiveLLMSystem: {str(e)}")
        return

    while True:
        user_input = input("> ")
        if user_input.lower() == "exit":
            break
        try:
            response = await system.process_input(user_input)
            print(f"System: {response}")
        except Exception as e:
            logger.error(f"Error processing input: {str(e)}")

    system.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
