from kafka import KafkaConsumer
import json
from memory_manager import MemoryManager

class MemoryConsumer:
    def __init__(self):
        self.consumer = KafkaConsumer(
            'scraped_data',
            bootstrap_servers='kafka:9092',
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest',  # Ensure you consume all messages
            enable_auto_commit=True,
            consumer_timeout_ms=1000  # Timeout after 1 second if no messages
        )
        self.memory_manager = MemoryManager()

    def consume(self):
        print("Starting MemoryConsumer...")
        try:
            while True:
                message_batch = self.consumer.poll(timeout_ms=1000)  # Poll for new messages
                if message_batch:
                    for _, messages in message_batch.items():
                        for message in messages:
                            data = message.value
                            title = data['title']
                            
                            if data is not None and title is not None:
                                # Example processing: Store in short-term memory
                                self.memory_manager.store_short_term(data)
                                print(f"Stored in Short-term Memory: {title}")
        except KeyboardInterrupt:
            print("Stopping MemoryConsumer...")

if __name__ == "__main__":
    consumer = MemoryConsumer()
    consumer.consume()
