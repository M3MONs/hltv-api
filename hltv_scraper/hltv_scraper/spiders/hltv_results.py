import scrapy
from .utils import parse_match


class HltvResultsSpider(scrapy.Spider):
    name = "hltv_results"
    allowed_domains = ["www.hltv.org"]
    start_urls = ["https://www.hltv.org/results?offset=0"]
    base_api_url = "https://www.hltv.org/results?offset={}"

    def parse_results(self, sublists):
        all_results = {}
        for sublist in sublists:
            date = sublist.css(".standard-headline::text").get()
            all_results[date] = [
                parse_match(result) for result in sublist.css("div.result")
            ]
        return all_results

    def parse(self, response):
        # TODO: check if offset was given
        sublists = response.css("div.allres .results-sublist")
        yield self.parse_results(sublists)
