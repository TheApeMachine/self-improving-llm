from nlu.nlu_pipeline import NLUPipeline
from prompt_optimization.prompt_optimizer import PromptOptimizer
from dynamic_mixture_of_experts.task_router import TaskRouter
from knowledge_graph.knowledge_graph import KnowledgeGraph
from knowledge_graph.memory_manager import MemoryManager
from scraping.spiders.wikipedia_spider import WikipediaSpider
import scrapy
from scrapy.crawler import CrawlerProcess

class SystemIntegration:
    def __init__(self):
        self.nlu_pipeline = NLUPipeline()
        self.prompt_optimizer = PromptOptimizer()
        self.task_router = TaskRouter()
        self.knowledge_graph = KnowledgeGraph()
        self.memory_manager = MemoryManager()
        self.crawler_process = CrawlerProcess()

    def run(self, prompt):
        # Step 1: NLU processing
        candidate_labels = ["scrape", "information", "explore"]
        nlu_result = self.nlu_pipeline.process_prompt(prompt, candidate_labels)
        
        # Step 2: Prompt Optimization
        optimized_prompt = self.prompt_optimizer.optimize_prompt(prompt, nlu_result['entities'])
        
        # Step 3: Task Routing
        task_result = self.task_router.route_task(optimized_prompt)
        
        # Step 4: Execute the Scraping Task if requested
        if "scrape" in nlu_result['intent']['labels']:
            print("Starting web scraping based on user input...")
            self.crawler_process.crawl(WikipediaSpider)
            self.crawler_process.start()
        
        # Example interaction: Prompt for feedback
        feedback = input("Was the information useful? (yes/no): ").strip().lower()
        if feedback == "no":
            print("Thank you for your feedback. We will improve.")
        
        return {
            "original_prompt": prompt,
            "nlu_result": nlu_result,
            "optimized_prompt": optimized_prompt,
            "task_result": task_result,
        }

if __name__ == "__main__":
    system = SystemIntegration()
    prompt = input("Please provide a prompt for the system: ")
    result = system.run(prompt)
    print(result)
