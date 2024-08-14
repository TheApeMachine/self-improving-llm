from kafka import KafkaConsumer
import json
from knowledge_graph import KnowledgeGraph

class KnowledgeGraphConsumer:
    def __init__(self):
        self.consumer = KafkaConsumer(
            'scraped_data',
            bootstrap_servers='kafka:9092',
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest',  # Ensure you consume all messages
            enable_auto_commit=True,
            consumer_timeout_ms=1000  # Timeout after 1 second if no messages
        )
        self.knowledge_graph = KnowledgeGraph()

    def consume(self):
        print("Starting KnowledgeGraphConsumer...")
        try:
            while True:
                message_batch = self.consumer.poll(timeout_ms=1000)  # Poll for new messages
                if message_batch:
                    for _, messages in message_batch.items():
                        for message in messages:
                            data = message.value
                            title = data['title']
                            content = data['content']

                            if title is not None and content is not None:
                                # Example processing: Add to knowledge graph
                                self.knowledge_graph.add_relationship(title, "mentions", content)
                                print(f"Processed and added to Knowledge Graph: {title}")
        except KeyboardInterrupt:
            print("Stopping KnowledgeGraphConsumer...")

if __name__ == "__main__":
    consumer = KnowledgeGraphConsumer()
    consumer.consume()
