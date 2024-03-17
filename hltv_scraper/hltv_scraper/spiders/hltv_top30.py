import scrapy


class HltvTop30Spider(scrapy.Spider):
    name = "hltv_top30"
    allowed_domains = ["www.hltv.org"]
    start_urls = ["https://www.hltv.org/ranking/teams"]

    def parse(self, response):
        ranked_teams = response.css("div.ranked-team.standard-box")

        for team in ranked_teams:
            position = team.css("span.position::text").get()
            name = team.css(".name::text").get()
            logo = team.css("span.team-logo img::attr(src)").get()
            points = team.css("span.points::text").get()
            players = team.css("div.playersLine .rankingNicknames span::text").getall()

            data = {
                "position": position if position else None,
                "name": name.strip() if name else None,
                "logo": logo.strip() if logo else None,
                "points": points.strip() if points else None,
                "players": players,
            }

            print(data)
            yield data
