import os, time, subprocess, json


def should_run_spider(json_name: str, hours: int = 1):
    localization = f"./hltv_scraper/{json_name}.json"
    if os.path.exists(localization) and time.time() - os.path.getmtime(localization) < (
        3600 * hours
    ):
        return False
    return True


def clear_old_data(json_name: str):
    open(f"./hltv_scraper/{json_name}.json", "w").close()


def run_spider(spider_name: str, json_name: str, args: str):
    if os.path.exists(f"./hltv_scraper/{json_name}.json"):
        clear_old_data(json_name)

    process = subprocess.Popen(
        ["scrapy", "crawl", spider_name] + args.split(),
        cwd="./hltv_scraper",
    )
    process.wait()


def get_profile_link(team_name: str):
    profiles_json = "./hltv_scraper/teams_profile.json"
    with open(profiles_json) as file:
        profiles = json.load(file)
        return profiles[team_name]


def get_players_profile(player: str):
    profiles_json = "./hltv_scraper/players_profiles.json"
    with open(profiles_json) as file:
        profiles = json.load(file)
        print(profiles)
        return profiles[player]


def is_team_profile_link(team_name: str):
    profiles_json = "./hltv_scraper/teams_profile.json"

    if not os.path.exists(profiles_json):
        return False

    with open(profiles_json) as file:
        profiles = json.load(file)
        if team_name in profiles:
            return True

    return False


def is_player_profiles(player_name: str):
    profiles_json = "./hltv_scraper/players_profiles.json"

    if not os.path.exists(profiles_json):
        return False

    with open(profiles_json) as file:
        profiles = json.load(file)
        if player_name in profiles:
            return True

    return False
