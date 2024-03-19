import scrapy
from .utils import parse_match


class HltvBigResultsSpider(scrapy.Spider):
    name = "hltv_big_results"
    allowed_domains = ["www.hltv.org"]
    start_urls = ["https://www.hltv.org/results?offset=0"]

    def parse(self, response):
        results = response.css("div.big-results .result-con")

        for result in results:
            data = parse_match(result)

            # print(data)
            yield data
