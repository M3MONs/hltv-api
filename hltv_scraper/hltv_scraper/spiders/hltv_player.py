from typing import Any
import scrapy
from .utils import parse_player_profile


class HltvPlayerSpider(scrapy.Spider):
    name = "hltv_player"
    allowed_domains = ["www.hltv.org"]

    def __init__(self, profile: str, **kwargs: Any):
        self.start_urls = [f"https://www.hltv.org{profile}"]
        super().__init__(**kwargs)

    def parse(self, response):
        profile = response.css("div.playerProfile")
        data = parse_player_profile(profile)
        yield data
