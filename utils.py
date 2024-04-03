import os, time, subprocess, json


def should_run_spider(json_name: str, hours: int = 1):
    localization = f"./hltv_scraper/{json_name}.json"
    if os.path.exists(localization) and time.time() - os.path.getmtime(localization) < (
        3600 * hours
    ):
        return False
    return True


def load_json_data(filename: str):
    with open(f"./hltv_scraper/{filename}.json", "r") as file:
        return json.load(file)


def is_profile_link(filename: str, profile: str):
    json_file = f"./hltv_scraper/{filename}.json"

    if not os.path.exists(json_file):
        return False

    with open(json_file) as file:
        profiles = json.load(file)
        if profile in profiles:
            return True

    return False


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
        return profiles[player]
