from typing import Any
import scrapy
from .parsers import ParsersFactory as PF


class HltvResultsSpider(scrapy.Spider):
    name = "hltv_results"
    allowed_domains = ["www.hltv.org"]

    def __init__(self, offset: int = 0, **kwargs: Any):
        self.start_urls = [f"https://www.hltv.org/results?offset={offset}"]
        super().__init__(**kwargs)

    def parse(self, response):
        sublists = response.css("div.allres .results-sublist")
        yield PF.get_parser("results").parse(sublists)
