from typing import Any
import scrapy


class HltvTeamSpider(scrapy.Spider):
    name = "hltv_team"
    allowed_domains = ["www.hltv.org"]

    def __init__(self, team_name="ence", **kwargs: Any):
        self.start_urls = [f"https://www.hltv.org/search?query={team_name}"]
        self.team_name = team_name.replace(" ", "-")
        super().__init__(**kwargs)

    def get_profile_link(self, response):
        return response.css(f'a[href$="/{self.team_name.lower()}"]').attrib["href"]

    def parse(self, response):
        profile_link = self.get_profile_link(response)
