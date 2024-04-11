import scrapy


class HltvMatchSpider(scrapy.Spider):
    name = "hltv_match"
    allowed_domains = ["www.hltv.org"]
    start_urls = ["https://www.hltv.org/matches"]

    def parse(self, response):
        pass
