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

    def parse_squad(self, response):
        players_container = response.css(".bodyshot-team.g-grid a.col-custom")

        return [
            {
                "name": player.css(".playerFlagName span.text-ellipsis::text").get(),
                "img": player.css("img.bodyshot-team-img::attr(src)").get(),
                "nation": f"https://www.hltv.org{player.css('img.flag::attr(src)').get()}",
            }
            for player in players_container
        ]

    def parse(self, response):
        profile_link = self.get_profile_link(response)
        if profile_link:
            yield scrapy.Request(
                url=f"https://www.hltv.org{profile_link}", callback=self.parse_profile
            )

    def parse_profile(self, response):
        team_data = {
            "name": response.css(".profile-team-name::text").get(),
            "ranking": response.css("span.right a::text").get(),
            "logo": response.css("img.teamlogo::attr(src)").get(),
            "country": response.css("div.team-country::text").get(),
            "country_img": f'https://www.hltv.org{response.css("div.team-country img::attr(src)").get()}',
            "squad": self.parse_squad(response),
        }
        if team_data["name"]:
            return team_data
