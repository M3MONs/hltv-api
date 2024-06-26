from typing import Any
import scrapy
from .utils import parse_match_teams_box, parse_map_holders, parse_table_stats


class HltvMatchSpider(scrapy.Spider):
    name = "hltv_match"
    allowed_domains = ["www.hltv.org"]

    def __init__(self, match: str, **kwargs: Any):
        self.start_urls = [f"https://www.hltv.org/matches/{match}"]
        super().__init__(**kwargs)

    def parse(self, response):
        teams_box = parse_match_teams_box(response.css(".teamsBox"))
        maps_score = parse_map_holders(response)
        player_stats = parse_table_stats(response.css("#all-content"))

        yield {"match": teams_box, "maps": maps_score, "stats": player_stats}
