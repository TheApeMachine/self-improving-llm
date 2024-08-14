from transformers import pipeline

class IntentRecognizer:
    def __init__(self, model_name='facebook/bart-large-mnli'):
        self.classifier = pipeline('zero-shot-classification', model=model_name)

    def recognize_intent(self, prompt, candidate_labels):
        return self.classifier(prompt, candidate_labels)

if __name__ == "__main__":
    recognizer = IntentRecognizer()
    prompt = "Book a table for two at an Italian restaurant tomorrow evening."
    labels = ["booking", "information", "reminder"]
    result = recognizer.recognize_intent(prompt, labels)
    print(result)
