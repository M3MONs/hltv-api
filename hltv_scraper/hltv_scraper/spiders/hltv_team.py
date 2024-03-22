from typing import Any
import scrapy


class HltvTeamSpider(scrapy.Spider):
    name = "hltv_team"
    allowed_domains = ["www.hltv.org"]
    start_urls = ["https://www.hltv.org/search?query="]

    def __init__(self, team_name="ENCE", **kwargs: Any):
        super().__init__(**kwargs)

    def parse(self, response):
        pass
