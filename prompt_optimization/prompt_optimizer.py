from .prompt_rephrasing import PromptRephraser
from .prompt_augmentation import PromptAugmentor

class PromptOptimizer:
    def __init__(self):
        self.rephraser = PromptRephraser()
        self.augmentor = PromptAugmentor()

    def optimize_prompt(self, prompt, entities):
        rephrased_prompt = self.rephraser.rephrase_prompt(prompt)
        optimized_prompt = self.augmentor.augment_prompt(rephrased_prompt, entities)
        return optimized_prompt

if __name__ == "__main__":
    optimizer = PromptOptimizer()
    prompt = "Book a table for two at an Italian restaurant tomorrow evening."
    entities = [{'word': 'Italian restaurant'}, {'word': 'tomorrow evening'}]
    result = optimizer.optimize_prompt(prompt, entities)
    print(result)
