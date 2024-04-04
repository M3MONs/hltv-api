import scrapy


class HltvNewsSpider(scrapy.Spider):
    name = "hltv_news"
    allowed_domains = ["www.hltv.org"]
    start_urls = ["https://www.hltv.org/news/archive"]

    def parse(self, response):
        pass
