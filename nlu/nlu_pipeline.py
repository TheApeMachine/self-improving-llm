from .intent_recognition import IntentRecognizer
from .entity_recognition import EntityRecognizer

class NLUPipeline:
    def __init__(self):
        self.intent_recognizer = IntentRecognizer()
        self.entity_recognizer = EntityRecognizer()

    def process_prompt(self, prompt, candidate_labels):
        intent = self.intent_recognizer.recognize_intent(prompt, candidate_labels)
        entities = self.entity_recognizer.recognize_entities(prompt)
        return {
            "intent": intent,
            "entities": entities
        }

if __name__ == "__main__":
    pipeline = NLUPipeline()
    prompt = "Book a table for two at an Italian restaurant tomorrow evening."
    labels = ["booking", "information", "reminder"]
    result = pipeline.process_prompt(prompt, labels)
    print(result)
