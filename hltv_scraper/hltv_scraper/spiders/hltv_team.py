from typing import Any
import scrapy
from .utils import parse_team_profile


class HltvTeamSpider(scrapy.Spider):
    name = "hltv_team"
    allowed_domains = ["www.hltv.org"]

    def __init__(self, team: str, **kwargs: Any):
        self.start_urls = [f"https://www.hltv.org{team}"]
        super().__init__(**kwargs)

    def parse(self, response):
        yield parse_team_profile(response)
