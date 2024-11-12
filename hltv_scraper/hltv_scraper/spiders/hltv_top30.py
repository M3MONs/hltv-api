import scrapy
from .parsers import ParsersFactory as PF


class HltvTop30Spider(scrapy.Spider):
    name = "hltv_top30"
    allowed_domains = ["www.hltv.org"]
    start_urls = ["https://www.hltv.org/ranking/teams"]

    def parse(self, response):
        ranked_teams = response.css("div.ranked-team.standard-box")

        for team in ranked_teams:
            data = PF.get_parser("team_ranking").parse(team)
            # print(data)
            yield data
