# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    default-jre \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all necessary files for the AI pipeline
COPY . /app

# Set the working directory for the AI pipeline
WORKDIR /app

# Command to run the AI pipeline
CMD ["python", "main.py"]
