import scrapy
from .utils import parse_team_ranking


class HltvTop30Spider(scrapy.Spider):
    name = "hltv_top30"
    allowed_domains = ["www.hltv.org"]
    start_urls = ["https://www.hltv.org/ranking/teams"]

    def parse(self, response):
        ranked_teams = response.css("div.ranked-team.standard-box")

        for team in ranked_teams:
            data = parse_team_ranking(team)
            # print(data)
            yield data
