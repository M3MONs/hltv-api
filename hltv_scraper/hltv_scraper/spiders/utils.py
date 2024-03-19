def parse_team(result, number):
    return {
        "name": result.css(f"div.team{number} .team::text").get(),
        "rounds": result.css(f"td.result-score span:nth-child({number})::text").get(),
        "logo": result.css(f"div.team{number} img::attr(src)").get(),
    }
