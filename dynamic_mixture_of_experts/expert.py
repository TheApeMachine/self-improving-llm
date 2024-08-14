class Expert:
    def __init__(self, name):
        self.name = name

    def process(self, task):
        raise NotImplementedError("Each expert must implement the 'process' method.")

class ExampleExpert(Expert):
    def process(self, task):
        # Example processing
        return f"Processed task '{task}' with expert '{self.name}'"

if __name__ == "__main__":
    expert = ExampleExpert(name="ExampleExpert")
    result = expert.process("Example Task")
    print(result)
