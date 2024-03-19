import scrapy


class HltvUpcomingMatchesSpider(scrapy.Spider):
    name = "hltv_upcoming_matches"
    allowed_domains = ["www.hltv.org"]
    start_urls = ["https://www.hltv.org/matches"]

    def parse(self, response):
        pass
