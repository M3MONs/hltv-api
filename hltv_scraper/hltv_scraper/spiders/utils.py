import json, os, scrapy


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


def update_json_data(filename: str, data: dict):
    file = f"{filename}.json"
    existing_data = {}

    try:
        if os.path.exists(file):
            with open(file, "r", encoding="utf-8") as f:
                existing_data = json.load(f)

        existing_data.update(data)

        with open(file, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, indent=4)

    except Exception as e:
        print(f"An error occurred while updating JSON data: {e}")


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


## HLTV_TEAMS_ID ##


def parse_teams_profile_link(response, team: str):
    teams = response.css(f"div.search a[href^='/team/']")
    return [
        {
            "name": team.css("a::text").get(),
            "img": team.css("a img::attr(src)").get(),
            "link": team.css("a::attr(href)").get(),
        }
        for team in teams
    ]


## HLTV_TEAM ##


def parse_team_squad(response):
    players_container = response.css(".bodyshot-team.g-grid a.col-custom")
    return [
        {
            "name": player.css(".playerFlagName span.text-ellipsis::text").get(),
            "img": player.css("img.bodyshot-team-img::attr(src)").get(),
            "nation": f"https://www.hltv.org{player.css('img.flag::attr(src)').get()}",
        }
        for player in players_container
    ]


def parse_team_profile(response):
    team_data = {
        "name": response.css(".profile-team-name::text").get(),
        "ranking": response.css("span.right a::text").get(),
        "logo": response.css("img.teamlogo::attr(src)").get(),
        "country": response.css("div.team-country::text").get(),
        "country_img": f'https://www.hltv.org{response.css("div.team-country img::attr(src)").get()}',
        "squad": parse_team_squad(response),
    }
    if team_data["name"]:
        return team_data


## HLTV_RESULTS ##


def parse_results(sublists):
    all_results = {}
    for sublist in sublists:
        date = sublist.css(".standard-headline::text").get()
        all_results[date] = [
            parse_match(result) for result in sublist.css("div.result")
        ]
    return all_results


## HLTV_PLAYERS_SEARCH


def parse_players_profile_link(response, player: str):
    return response.css(f"a[href^='/player/'][href$='/{player}']").getall()


def parse_players_profile(profiles):
    profiles_data = []
    for profile in profiles:
        selector = scrapy.Selector(text=profile)
        data = {
            "name": selector.css("a::text").get(),
            "profile_link": selector.css("a::attr(href)").get(),
            "img": selector.css("img::attr(src)").get(),
        }
        profiles_data.append(data)
    return profiles_data


## HLTV_NEWS ##


def parse_news(articles):
    return [
        {
            "title": article.css(".newstext::text").get(),
            "img": article.css("img.newsflag::attr(src)").get(),
            "date": article.css("div.newsrecent::text").get(),
            "comments": article.css("div.newstc div:nth-child(2)::text").get(),
        }
        for article in articles
    ]


## HLTV_PLAYER ##


def parse_player_stats(stats):
    return [
        {
            f'{stat.css("b::text").get()}': stat.css("span.statsVal p::text").get(),
        }
        for stat in stats
    ]


def parse_player_trophies(trophies):
    return [
        {
            "title": trophy.css("span.trophyDescription::attr(title)").get(),
            "icon": trophy.css("span.trophyDescription img::attr(src)").get(),
        }
        for trophy in trophies
    ]


def parse_player_profile(profile):
    return {
        "nick": profile.css("h1.playerNickname::text").get(),
        "name": profile.css("div.playerRealname::text").get(),
        "flag": profile.css("div.playerRealname img::attr(src)").get(),
        "team": profile.css('div.playerTeam span[itemprop="text"] ::text').getall(),
        "stats": parse_player_stats(profile.css("div.player-stat")),
        "trophies": parse_player_trophies(profile.css(".trophy")),
    }
