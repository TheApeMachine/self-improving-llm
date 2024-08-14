import scrapy
from kafka import KafkaProducer
import json

class WikipediaSpider(scrapy.Spider):
    name = "wikipedia"
    start_urls = [
        'https://en.wikipedia.org/wiki/Artificial_intelligence',
        'https://en.wikipedia.org/wiki/Machine_learning',
    ]

    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers='kafka:9092',
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def parse(self, response):
        title = response.css('h1::text').get()
        headings = response.css('h2 .mw-headline::text').extract()
        content = ' '.join(response.css('p::text').extract())
        
        # Send the data to Kafka
        self.producer.send('scraped_data', {
            'title': title,
            'headings': headings,
            'content': content,
            'url': response.url
        })
        
        # Follow links to other articles
        for link in response.css('a::attr(href)').extract():
            if link.startswith('/wiki/') and ':' not in link:
                yield response.follow(link, self.parse)
        
        print(f"Sent data to Kafka for article: {title}")