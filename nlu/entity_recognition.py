from transformers import pipeline

class EntityRecognizer:
    def __init__(self, model_name='dbmdz/bert-large-cased-finetuned-conll03-english'):
        self.ner = pipeline('ner', model=model_name)

    def recognize_entities(self, prompt):
        return self.ner(prompt)

if __name__ == "__main__":
    recognizer = EntityRecognizer()
    prompt = "Book a table for two at an Italian restaurant tomorrow evening."
    result = recognizer.recognize_entities(prompt)
    print(result)
