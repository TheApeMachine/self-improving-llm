# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    openjdk-11-jdk-headless \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the spider into the Scrapy project
COPY scraping/wikipedia /app/wikipedia/

# Set the working directory to the Scrapy project
WORKDIR /app

# Expose port (optional, depending on your services)
EXPOSE 5000

# Command to run your app
CMD ["scrapy", "crawl", "wikipedia"]
