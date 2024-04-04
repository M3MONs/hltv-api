import scrapy
from .utils import parse_results


class HltvResultsSpider(scrapy.Spider):
    name = "hltv_results"
    allowed_domains = ["www.hltv.org"]
    start_urls = ["https://www.hltv.org/results?offset=0"]
    base_api_url = "https://www.hltv.org/results?offset={}"

    def parse(self, response):
        sublists = response.css("div.allres .results-sublist")
        yield parse_results(sublists)
