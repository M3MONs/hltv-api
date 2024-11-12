import scrapy
from .parsers import ParsersFactory as PF


class HltvUpcomingMatchesSpider(scrapy.Spider):
    name = "hltv_upcoming_matches"
    allowed_domains = ["www.hltv.org"]
    start_urls = ["https://www.hltv.org/matches"]

    def parse(self, response):
        matches_sections = response.css("div.upcomingMatchesSection")
        all_matches = {}

        for section in matches_sections:
            date = section.css(".matchDayHeadline::text").get()

            all_matches[date] = [
                PF.get_parser("upcoming_match").parse(match)
                for match in section.css("div.upcomingMatch")
            ]

        yield all_matches
