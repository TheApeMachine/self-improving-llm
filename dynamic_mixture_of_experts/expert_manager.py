from .expert import Expert, ExampleExpert

class ExpertManager:
    def __init__(self):
        self.experts = {}

    def create_expert(self, name):
        expert = ExampleExpert(name)
        self.experts[name] = expert
        return expert

    def get_expert(self, name):
        return self.experts.get(name)
