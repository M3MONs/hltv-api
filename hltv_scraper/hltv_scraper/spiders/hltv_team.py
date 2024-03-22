import scrapy


class HltvTeamSpider(scrapy.Spider):
    name = "hltv_team"
    allowed_domains = ["www.hltv.org"]
    start_urls = ["https://www.hltv.org/search?query="]

    def parse(self, response):
        pass
