class MemoryManager:
    def __init__(self):
        self.short_term_memory = []
        self.long_term_memory = []
        self.shared_memory = {}

    def store_short_term(self, data):
        self.short_term_memory.append(data)

    def store_long_term(self, data):
        self.long_term_memory.append(data)

    def store_shared(self, key, data):
        self.shared_memory[key] = data

    def retrieve_shared(self, key):
        return self.shared_memory.get(key)

if __name__ == "__main__":
    mm = MemoryManager()
    mm.store_short_term("Short-term memory example")
    mm.store_long_term("Long-term memory example")
    mm.store_shared("shared_key", "Shared memory example")
    print(mm.short_term_memory)
    print(mm.long_term_memory)
    print(mm.retrieve_shared("shared_key"))
