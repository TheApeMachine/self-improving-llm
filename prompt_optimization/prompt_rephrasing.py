from transformers import pipeline

class PromptRephraser:
    def __init__(self, model_name='tuner007/pegasus_paraphrase'):
        self.paraphraser = pipeline('text2text-generation', model=model_name)

    def rephrase_prompt(self, prompt):
        paraphrase = self.paraphraser(prompt, num_return_sequences=1, num_beams=5)
        return paraphrase[0]['generated_text']

if __name__ == "__main__":
    rephraser = PromptRephraser()
    prompt = "Book a table for two at an Italian restaurant tomorrow evening."
    result = rephraser.rephrase_prompt(prompt)
    print(result)
