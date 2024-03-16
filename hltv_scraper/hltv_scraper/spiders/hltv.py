import scrapy


class HltvSpider(scrapy.Spider):
    name = "hltv"
    allowed_domains = ["hltv.org"]
    start_urls = ["https://hltv.org"]

    def parse(self, response):
        pass
