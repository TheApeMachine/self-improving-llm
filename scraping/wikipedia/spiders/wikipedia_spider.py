import scrapy
from kafka import KafkaProducer
import json
from fp.fp import FreeProxy
from fake_useragent import UserAgent
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message
import time
import random

class RotatingProxyMiddleware:
    def __init__(self, crawler):
        self.crawler = crawler
        self.proxies = self.load_proxies()
        self.current_proxy = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def load_proxies(self):
        return [FreeProxy().get() for _ in range(10)]  # Load 10 proxies

    def process_request(self, request, spider):
        if not self.current_proxy or self.crawler.stats.get_value('proxy/banned_count', 0) > 3:
            self.current_proxy = random.choice(self.proxies)
            self.crawler.stats.set_value('proxy/banned_count', 0)
            print(f"Using proxy: {self.current_proxy}")
        request.meta['proxy'] = self.current_proxy

    def process_response(self, request, response, spider):
        if response.status in [403, 503]:
            self.crawler.stats.inc_value('proxy/banned_count')
        return response

class CustomRetryMiddleware(RetryMiddleware):
    def process_response(self, request, response, spider):
        if response.status in [403, 503]:
            reason = response_status_message(response.status)
            print(f"Retrying request: {request.url}")
            return self._retry(request, reason, spider) or response
        return response

class WikipediaSpider(scrapy.Spider):
    name = "wikipedia"
    start_urls = [
        'https://en.wikipedia.org/wiki/Artificial_intelligence',
        'https://en.wikipedia.org/wiki/Machine_learning',
    ]

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'wikipedia.spiders.wikipedia_spider.RotatingProxyMiddleware': 610,
            'wikipedia.spiders.wikipedia_spider.CustomRetryMiddleware': 620,
        },
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY': 5,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
    }

    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers='kafka:9092',
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.ua = UserAgent()

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, headers={'User-Agent': self.ua.random}, callback=self.parse)

    def parse(self, response):
        title = response.css('h1::text').get()
        headings = response.css('h2 .mw-headline::text').extract()
        content = ' '.join(response.css('p::text').extract())

        print(f"Scraped: {title}")
        
        # Send the data to Kafka
        self.producer.send('scraped_data', {
            'title': title,
            'headings': headings,
            'content': content,
            'url': response.url
        })
        
        # Follow links to other articles
        for link in response.css('a::attr(href)').extract():
            if link not in link:
                yield response.follow(link, self.parse, headers={'User-Agent': self.ua.random})

        # Implement a delay between requests
        time.sleep(random.uniform(1, 3))