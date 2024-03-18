import scrapy


class HltvResultsSpider(scrapy.Spider):
    name = "hltv_results"
    allowed_domains = ["www.hltv.org"]
    start_urls = ["https://www.hltv.org/results?offset=0"]
    base_api_url = "https://www.hltv.org/results?offset={}"

    def parse_team(self, result, number):
        name = result.css(f"div.team{number} .team::text").get()
        rounds = result.css(f"td.result-score span:nth-child({number})::text").get()
        logo = result.css(f"div.team{number} img::attr(src)").get()
        return {"name": name, "rounds": rounds, "logo": logo}

    def parse_match(self, result):
        map = result.css("div.map-text::text").get()
        event = result.css("span.event-name::text").get()
        first_team = self.parse_team(result, 1)
        second_team = self.parse_team(result, 2)
        match = {"map": map, "event": event, "team1": first_team, "team2": second_team}
        return match

    def parse_results(self, sublists):
        all_results = []
        for sublist in sublists:
            results = sublist.css("div.result")
            for result in results:
                all_results.append(self.parse_match(result))
        return all_results

    def parse(self, response):
        # TODO: check if offset was given
        sublists = response.css("div.results-sublist")
        results = self.parse_results(sublists)
        # print(results)
        yield {"results": results}
