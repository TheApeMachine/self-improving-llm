# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the consumer files
COPY . /app/kafka_consumers

# Set the working directory
WORKDIR /app

# Command to run the knowledge graph consumer
CMD ["python", "kafka_consumers/knowledge_graph_consumer.py"]
