def parse_team(result, number):
    return {
        "name": result.css(f"div.team{number} .team::text").get(),
        "score": result.css(f"td.result-score span:nth-child({number})::text").get(),
        "logo": result.css(f"div.team{number} img::attr(src)").get(),
    }


def parse_match(result):
    return {
        "map": result.css("div.map-text::text").get(),
        "event": result.css("span.event-name::text").get(),
        "team1": parse_team(result, 1),
        "team2": parse_team(result, 2),
    }
