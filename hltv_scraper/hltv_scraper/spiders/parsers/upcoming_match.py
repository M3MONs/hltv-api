from .parser import Parser
from .upcoming_match_team import UpcomingMatchTeamParser as UMTP
from ..utils import is_team_in_upcoming_match

class UpcomingMatchParser(Parser):
    @staticmethod
    def parse(match):
        if is_team_in_upcoming_match(match):
            return {
                "hour": match.css("div.matchTime::text").get(),
                "meta": match.css("div.matchMeta::text").get(),
                "event": match.css("div.matchEventName::text").get(),
                "team1": UMTP.parse(match, 1),
                "team2": UMTP.parse(match, 2),
            }