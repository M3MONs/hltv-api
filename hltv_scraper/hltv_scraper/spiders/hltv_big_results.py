import scrapy


class HltvBigResultsSpider(scrapy.Spider):
    name = "hltv_big_results"
    allowed_domains = ["www.hltv.org"]
    start_urls = ["https://www.hltv.org/results?offset=0"]

    def parse_team(self, result, number):
        name = result.css(f"div.team{number} .team::text").get()
        rounds = result.css(f"td.result-score span:nth-child({number})::text").get()
        logo = result.css(f"div.team{number} img::attr(src)").get()
        return {"name": name, "rounds": rounds, "logo": logo}

    def parse(self, response):
        results = response.css("div.big-results .result-con")

        for result in results:
            first_team = self.parse_team(result, 1)
            second_team = self.parse_team(result, 2)
            map_name = result.css("div.map-text::text").get()
            event = result.css("span.event-name::text").get()

            data = {
                "team-1": first_team,
                "team-2": second_team,
                "map": map_name,
                "event": event,
            }

            # print(data)
            yield data
