from abc import ABC, abstractmethod


# Base model interface
class BaseModel(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass
