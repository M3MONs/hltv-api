import scrapy


class HltvPlayerSpider(scrapy.Spider):
    name = "hltv_player"
    allowed_domains = ["www.hltv.org"]
    start_urls = ["https://www.hltv.org"]

    def parse(self, response):
        pass
