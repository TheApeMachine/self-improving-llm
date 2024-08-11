import deeplake
from loguru import logger


class MemorySystem:
    def __init__(self):
        self.ds = deeplake.dataset("./memories", overwrite=True)
        if "prompt" not in self.ds.tensors:
            self.ds.create_tensor("prompt", htype="text")
        if "response" not in self.ds.tensors:
            self.ds.create_tensor("response", htype="text")
        if "feedback" not in self.ds.tensors:
            self.ds.create_tensor("feedback", htype="text")

        logger.debug("[Memory System] Initialized DeepLake memory system.")

    def store_interaction(self, prompt: str, response: str, feedback: str = None):
        self.ds["prompt"].append(prompt)
        self.ds["response"].append(response)
        if feedback is not None:
            self.ds["feedback"].append(feedback)
        else:
            self.ds["feedback"].append("")  # Append empty string if no feedback

        logger.debug(
            f"[Memory System] Stored interaction with prompt: {prompt} and response: {response}."
        )

    def retrieve_past_interactions(self, query: str):
        logger.debug(f"[Memory System] Retrieving past interactions for query: {query}")
        # Implement retrieval logic (e.g., vector-based search)
        # For now, just returning empty for illustration
        return []
