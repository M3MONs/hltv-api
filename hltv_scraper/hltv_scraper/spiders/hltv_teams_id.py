import scrapy


class HltvTeamsIdSpider(scrapy.Spider):
    name = "hltv_teams_id"
    allowed_domains = ["www.hltv.org"]
    start_urls = ["https://www.hltv.org/search?query="]

    def parse(self, response):
        pass
