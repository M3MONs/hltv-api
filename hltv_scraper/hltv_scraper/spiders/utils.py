def parse_team(result, number):
    return {
        "name": result.css(f"div.team{number} .team::text").get(),
        "score": result.css(f"td.result-score span:nth-child({number})::text").get(),
        "logo": result.css(f"div.team{number} img::attr(src)").get(),
    }


def parse_team_ranking(team):
    return {
        "position": team.css("span.position::text").get(),
        "name": team.css(".name::text").get(),
        "logo": team.css("span.team-logo img::attr(src)").get(),
        "points": team.css("span.points::text").get(),
        "players": team.css("div.playersLine .rankingNicknames span::text").getall(),
    }


def parse_match(result):
    return {
        "map": result.css("div.map-text::text").get(),
        "event": result.css("span.event-name::text").get(),
        "team1": parse_team(result, 1),
        "team2": parse_team(result, 2),
    }


## HLTV_UPCOMING_MATCHES ##


def parse_upcoming_match_team(match, number):
    return {
        "name": match.css(f"div.team{number} .matchTeamName::text").get(),
        "logo": match.css(f"div.team{number} img::attr(src)").get(),
    }


def is_team_in_upcoming_match(match):
    return match.css("div.team1 .matchTeamName::text").get() is not None


def parse_upcoming_match(match):
    print(is_team_in_upcoming_match(match))
    if is_team_in_upcoming_match(match):
        return {
            "hour": match.css("div.matchTime::text").get(),
            "meta": match.css("div.matchMeta::text").get(),
            "event": match.css("div.matchEventName::text").get(),
            "team1": parse_upcoming_match_team(match, 1),
            "team2": parse_upcoming_match_team(match, 2),
        }
