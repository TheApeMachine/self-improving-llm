from selenium import webdriver
from loguru import logger
from rich.logging import RichHandler
import time

# Set up pretty logging
logger.remove()
logger.add(RichHandler(), format="{message}", level="DEBUG")


# Headless browser for real-time information sourcing
class HeadlessBrowser:
    def __init__(self):
        self.driver = (
            webdriver.Firefox()
        )  # Or use Chrome, with appropriate driver setup
        logger.debug("[Headless Browser] Initialized headless browser.")

    def fetch_data(self, url: str):
        logger.debug(f"[Headless Browser] Fetching data from {url}")
        self.driver.get(url)
        time.sleep(3)  # Wait for the page to load
        page_content = self.driver.page_source
        logger.debug(f"[Headless Browser] Fetched data from {url}")
        return page_content

    def close(self):
        logger.debug("[Headless Browser] Closing browser.")
        self.driver.quit()
