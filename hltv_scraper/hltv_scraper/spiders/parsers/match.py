from .parser import Parser
from .team import TeamParser


class MatchParser(Parser):
    @staticmethod
    def parse(result):
        return {
            "link": result.css("a.a-reset::attr(href)").get(),
            "map": result.css("div.map-text::text").get(),
            "event": result.css("span.event-name::text").get(),
            "team1": TeamParser.parse(result, 1),
            "team2": TeamParser.parse(result, 2),
        }
