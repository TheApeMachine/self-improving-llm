from kafka import KafkaProducer, KafkaConsumer

def create_producer():
    return KafkaProducer(bootstrap_servers='kafka:9092')

def create_consumer(topic):
    return KafkaConsumer(topic, bootstrap_servers='kafka:9092', auto_offset_reset='earliest')

if __name__ == "__main__":
    producer = create_producer()
    producer.send('test_topic', b'This is a test message')
    print("Test message sent to Kafka")
