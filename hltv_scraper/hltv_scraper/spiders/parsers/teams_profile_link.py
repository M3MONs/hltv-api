from .parser import Parser

class TeamProfileLinkParser(Parser):
    @staticmethod
    def parse(response):
        teams = response.css(f"div.search a[href^='/team/']")
        return [
            {
                "name": team.css("a::text").get(),
                "img": team.css("a img::attr(src)").get(),
                "link": team.css("a::attr(href)").get(),
            }
            for team in teams
        ]