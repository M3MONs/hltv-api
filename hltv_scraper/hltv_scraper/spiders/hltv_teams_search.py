import scrapy
from typing import Any
from .utils import update_json_data, parse_teams_profile_link


class HltvTeamsSearchSpider(scrapy.Spider):
    name = "hltv_teams_search"
    allowed_domains = ["www.hltv.org"]

    def __init__(self, team: str, **kwargs: Any):
        self.start_urls = [f"https://www.hltv.org/search?query={team}"]
        self.team_name = team
        super().__init__(**kwargs)

    def parse(self, response):
        profile_link = parse_teams_profile_link(response, self.team_name)
        if profile_link:
            data = {f"{self.team_name}": profile_link}
            update_json_data("teams_profile", data)
