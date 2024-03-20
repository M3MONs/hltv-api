import scrapy


class HltvUpcomingMatchesSpider(scrapy.Spider):
    name = "hltv_upcoming_matches"
    allowed_domains = ["www.hltv.org"]
    start_urls = ["https://www.hltv.org/matches"]

    def is_match_teams(self, match):
        return match.css("div.team1 .matchTeamName::text").get() is not None

    def parse_team(self, match, number):
        return {
            "name": match.css(f"div.team{number} .matchTeamName::text").get(),
            "logo": match.css(f"div.team{number} img::attr(src)").get(),
        }

    def parse_match(self, match):
        if self.is_match_teams(match):
            return {
                "hour": match.css("div.matchTime::text").get(),
                "meta": match.css("div.matchMeta::text").get(),
                "team1": self.parse_team(match, 1),
                "team2": self.parse_team(match, 2),
            }

    def parse(self, response):
        matches_sections = response.css("div.upcomingMatchesSection")
        all_matches = {}

        for section in matches_sections:
            date = section.css(".matchDayHeadline::text").get()

            all_matches[date] = [
                self.parse_match(match) for match in section.css("div.upcomingMatch")
            ]

        yield all_matches
