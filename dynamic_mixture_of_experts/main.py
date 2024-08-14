from nlu.nlu_pipeline import NLUPipeline
from prompt_optimization.prompt_optimizer import PromptOptimizer
from dynamic_mixture_of_experts.task_router import TaskRouter
from knowledge.memory_manager import MemoryManager
from knowledge.knowledge_graph import KnowledgeGraph

class AIPipeline:
    def __init__(self):
        self.nlu_pipeline = NLUPipeline()
        self.prompt_optimizer = PromptOptimizer()
        self.task_router = TaskRouter()
        self.memory_manager = MemoryManager()
        self.knowledge_graph = KnowledgeGraph()

    def run(self, prompt):
        # Step 1: NLU processing
        nlu_result = self.nlu_pipeline.process_prompt(prompt, candidate_labels=["task", "query", "reminder"])
        
        # Step 2: Prompt Optimization
        optimized_prompt = self.prompt_optimizer.optimize_prompt(prompt, nlu_result['entities'])
        
        # Step 3: Task Routing
        task_result = self.task_router.route_task(optimized_prompt)
        
        # Step 4: Process and store the result (example: store in memory)
        self.memory_manager.store_short_term(task_result)
        
        # Example output
        print(f"Final Result: {task_result}")
        return task_result

if __name__ == "__main__":
    pipeline = AIPipeline()
    user_prompt = input("Enter a prompt: ")
    pipeline.run(user_prompt)
