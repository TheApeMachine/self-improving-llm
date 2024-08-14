class PromptAugmentor:
    def augment_prompt(self, prompt, entities):
        # Simple example of augmentation by including identified entities
        if entities:
            entity_str = ', '.join([entity['word'] for entity in entities])
            return f"{prompt}. Identified entities: {entity_str}"
        return prompt

if __name__ == "__main__":
    augmentor = PromptAugmentor()
    prompt = "Book a table for two at an Italian restaurant tomorrow evening."
    entities = [{'word': 'Italian restaurant'}, {'word': 'tomorrow evening'}]
    result = augmentor.augment_prompt(prompt, entities)
    print(result)
