import scrapy


class HltvPlayersSearchSpider(scrapy.Spider):
    name = "hltv_players_search"
    allowed_domains = ["www.hltv.org"]
    start_urls = ["https://www.hltv.org/search?query="]

    def parse(self, response):
        pass
