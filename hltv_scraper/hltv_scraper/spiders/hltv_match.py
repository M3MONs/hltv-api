import scrapy
from typing import Any
from scrapy_selenium import SeleniumRequest
from .parsers import ParsersFactory as PF


class HltvMatchSpider(scrapy.Spider):
    name = "hltv_match"
    allowed_domains = ["www.hltv.org"]

    def __init__(self, match: str, **kwargs: Any):
        self.start_urls = [f"https://www.hltv.org/matches/{match}"]
        super().__init__(**kwargs)

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(
                url=url,
                callback=self.parse,
            )

    def parse(self, response):
        teams_box = PF.get_parser("match_teams_box").parse(response.css(".teamsBox"))
        maps_score = PF.get_parser("map_holders").parse(response)
        player_stats = PF.get_parser("table_stats").parse(response.css("#all-content"))

        yield {"match": teams_box, "maps": maps_score, "stats": player_stats}
