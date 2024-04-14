import scrapy


class HltvTeamMatchesSpider(scrapy.Spider):
    name = "hltv_team_matches"
    allowed_domains = ["www.hltv.org"]
    start_urls = ["https://www.hltv.org/results?team="]

    def parse(self, response):
        pass
