import scrapy
from .utils import parse_team


class HltvResultsSpider(scrapy.Spider):
    name = "hltv_results"
    allowed_domains = ["www.hltv.org"]
    start_urls = ["https://www.hltv.org/results?offset=0"]
    base_api_url = "https://www.hltv.org/results?offset={}"

    def parse_match(self, result):
        return {
            "map": result.css("div.map-text::text").get(),
            "event": result.css("span.event-name::text").get(),
            "team1": parse_team(result, 1),
            "team2": parse_team(result, 2),
        }

    def parse_results(self, sublists):
        all_results = {}
        for sublist in sublists:
            date = sublist.css(".standard-headline::text").get()
            all_results[date] = [
                self.parse_match(result) for result in sublist.css("div.result")
            ]
        return all_results

    def parse(self, response):
        # TODO: check if offset was given
        sublists = response.css("div.allres .results-sublist")
        yield self.parse_results(sublists)
