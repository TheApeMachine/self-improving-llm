import os
from transformers import AutoModelForCausalLM, AutoTokenizer
from loguru import logger
from rich.logging import RichHandler

# Set up pretty logging
logger.remove()
logger.add(RichHandler(), format="{message}", level="DEBUG")

class ReasoningModel:
    def __init__(self, model_name="gpt2"):  # Using GPT-2 as a default model
        self.model_name = model_name
        self.hf_token = os.getenv("HF_API_TOKEN")
        
        if not self.hf_token:
            logger.warning("HF_API_TOKEN not found in environment variables. Some models may not be accessible.")
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, use_auth_token=self.hf_token)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name, use_auth_token=self.hf_token)
            logger.debug(f"[Reasoning Model] Initialized with model {self.model_name}")
        except Exception as e:
            logger.error(f"[Reasoning Model] Error initializing model {self.model_name}: {str(e)}")
            raise

    def generate(self, prompt: str, max_length: int = 100) -> str:
        try:
            logger.debug(f"[Reasoning Model] Generating response for prompt: {prompt}")
            inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
            outputs = self.model.generate(**inputs, max_length=max_length, num_return_sequences=1)
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            logger.debug(f"[Reasoning Model] Generated response: {response}")
            return response
        except Exception as e:
            logger.error(f"[Reasoning Model] Error generating response: {str(e)}")
            return f"Error generating response: {str(e)}"
