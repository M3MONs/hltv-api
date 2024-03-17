import scrapy


class HltvBigResultsSpider(scrapy.Spider):
    name = "hltv_big_results"
    allowed_domains = ["www.hltv.org"]
    start_urls = ["https://www.hltv.org/results?offset=0"]

    def parse(self, response):
        pass
