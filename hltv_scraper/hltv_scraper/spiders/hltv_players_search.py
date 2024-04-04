from typing import Any
import scrapy
from .utils import update_json_data, parse_players_profile_link, parse_players_profile


class HltvPlayersSearchSpider(scrapy.Spider):
    name = "hltv_players_search"
    allowed_domains = ["www.hltv.org"]

    def __init__(self, player: str | None = None, **kwargs: Any):
        self.start_urls = [f"https://www.hltv.org/search?query={player}"]
        self.player_search = player
        super().__init__(**kwargs)

    def parse(self, response):
        profiles = parse_players_profile_link(response, self.player_search)

        if not profiles:
            return

        extracted_profiles = parse_players_profile(profiles)

        if extracted_profiles:
            data = {f"{self.player_search}": extracted_profiles}
            update_json_data("players_profiles", data)
