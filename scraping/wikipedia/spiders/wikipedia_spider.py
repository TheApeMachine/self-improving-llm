import scrapy

class WikipediaSpider(scrapy.Spider):
    name = "wikipedia"
    start_urls = [
        'https://en.wikipedia.org/wiki/Main_Page',
    ]

    def parse(self, response):
        for link in response.css('a::attr(href)').extract():
            if link.startswith('/wiki/') and ':' not in link:
                yield response.follow(link, self.parse_article)

    def parse_article(self, response):
        title = response.css('h1::text').get()
        content = ' '.join(response.css('p::text').extract())
        yield {
            'title': title,
            'content': content,
            'url': response.url,
        }
