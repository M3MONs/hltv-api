from typing import Any
import scrapy


class HltvTeamSpider(scrapy.Spider):
    name = "hltv_team"
    allowed_domains = ["www.hltv.org"]

    def __init__(self, team_name="ENCE", **kwargs: Any):
        self.start_urls = [f"https://www.hltv.org/search?query={team_name}"]
        super().__init__(**kwargs)

    def parse(self, response):
        pass
