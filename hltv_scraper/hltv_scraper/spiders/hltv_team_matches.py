from typing import Any
import scrapy
from .utils import parse_team_results


class HltvTeamMatchesSpider(scrapy.Spider):
    name = "hltv_team_matches"
    allowed_domains = ["www.hltv.org"]

    def __init__(self, id: str, offset: int = 0, **kwargs: Any):
        self.start_urls = [f"https://www.hltv.org/results?offset={offset}&team={id}"]
        super().__init__(**kwargs)

    def parse(self, response):
        results = response.css(".results-all .a-reset")
        data = parse_team_results(results)
        yield from data
