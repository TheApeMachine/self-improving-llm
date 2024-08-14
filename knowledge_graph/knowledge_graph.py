class KnowledgeGraph:
    def __init__(self):
        self.graph = {}

    def add_relationship(self, entity1, relationship, entity2):
        if entity1 not in self.graph:
            self.graph[entity1] = {}
        if relationship not in self.graph[entity1]:
            self.graph[entity1][relationship] = []
        self.graph[entity1][relationship].append(entity2)

    def query_relationship(self, entity1, relationship):
        return self.graph.get(entity1, {}).get(relationship, [])

if __name__ == "__main__":
    kg = KnowledgeGraph()
    kg.add_relationship("AI", "is a field of", "Computer Science")
    result = kg.query_relationship("AI", "is a field of")
    print(result)
