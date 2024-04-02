from typing import Any
import scrapy, os, json


class HltvPlayersSearchSpider(scrapy.Spider):
    name = "hltv_players_search"
    allowed_domains = ["www.hltv.org"]

    def __init__(self, player: str | None = None, **kwargs: Any):
        self.start_urls = [f"https://www.hltv.org/search?query={player}"]
        self.player_search = player
        super().__init__(**kwargs)

    def extract_profiles(self, profiles):
        profiles_data = []
        for profile in profiles:
            selector = scrapy.Selector(text=profile)
            data = {
                "name": selector.css("a::text").get(),
                "profile_link": selector.css("a::attr(href)").get(),
                "img": selector.css("img::attr(src)").get(),
            }
            profiles_data.append(data)
        return profiles_data

    def get_profiles_link(self, response):
        return response.css(
            f"a[href^='/player/'][href$='/{self.player_search}']"
        ).getall()

    def save_to_json(self, data):
        file_path = "players_profiles.json"
        existing_data = {}

        if os.path.exists(file_path):
            with open(file_path, "r") as json_file:
                existing_data = json.load(json_file)

        existing_data.update(data)

        with open(file_path, "w", encoding="utf-8") as json_file:
            json.dump(existing_data, json_file, indent=4, ensure_ascii=False)

    def parse(self, response):
        profiles = self.get_profiles_link(response)
        if not profiles:
            return
        data = self.extract_profiles(profiles)
        if data:
            self.save_to_json({f"{self.player_search}": data})
