import scrapy, json, os
from typing import Any


class HltvTeamsIdSpider(scrapy.Spider):
    name = "hltv_teams_id"
    allowed_domains = ["www.hltv.org"]

    def __init__(self, team: str, **kwargs: Any):
        self.start_urls = [f"https://www.hltv.org/search?query={team}"]
        self.team_name = team
        super().__init__(**kwargs)

    def get_profile_link(self, response):
        return response.css(
            f"a[href^='/team/'][href$='/{self.team_name.replace('+', '-')}']::attr(href)"
        ).get()

    def save_to_json(self, data):
        existing_data = {}

        if os.path.exists("teams_profile.json"):
            with open("teams_profile.json", "r") as json_file:
                existing_data = json.load(json_file)

        existing_data.update(data)

        with open("teams_profile.json", "w") as json_file:
            json.dump(existing_data, json_file, indent=4)

    def parse(self, response):
        profile_link = self.get_profile_link(response)
        if profile_link:
            self.save_to_json({f"{self.team_name}": profile_link})
