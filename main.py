from nlu.nlu_pipeline import NLUPipeline
from prompt_optimization.prompt_optimizer import PromptOptimizer
from dynamic_mixture_of_experts.task_router import TaskRouter
from knowledge_graph.knowledge_graph import KnowledgeGraph
from knowledge_graph.memory_manager import MemoryManager

class SystemIntegration:
    def __init__(self):
        self.nlu_pipeline = NLUPipeline()
        self.prompt_optimizer = PromptOptimizer()
        self.task_router = TaskRouter()
        self.knowledge_graph = KnowledgeGraph()
        self.memory_manager = MemoryManager()

    def run(self, prompt):
        # Step 1: NLU processing
        candidate_labels = ["booking", "information", "reminder"]
        nlu_result = self.nlu_pipeline.process_prompt(prompt, candidate_labels)
        
        # Step 2: Prompt Optimization
        optimized_prompt = self.prompt_optimizer.optimize_prompt(prompt, nlu_result['entities'])
        
        # Step 3: Task Routing
        task_result = self.task_router.route_task(optimized_prompt)
        
        # Step 4: Knowledge Graph Interaction
        self.knowledge_graph.add_relationship("AI", "is a field of", "Computer Science")
        knowledge_result = self.knowledge_graph.query_relationship("AI", "is a field of")
        
        # Step 5: Memory Management
        self.memory_manager.store_short_term(task_result)
        self.memory_manager.store_shared("last_task_result", task_result)
        shared_memory_result = self.memory_manager.retrieve_shared("last_task_result")
        
        return {
            "original_prompt": prompt,
            "nlu_result": nlu_result,
            "optimized_prompt": optimized_prompt,
            "task_result": task_result,
            "knowledge_result": knowledge_result,
            "shared_memory_result": shared_memory_result
        }

if __name__ == "__main__":
    system = SystemIntegration()
    prompt = "Book a table for two at an Italian restaurant tomorrow evening."
    result = system.run(prompt)
    print(result)
