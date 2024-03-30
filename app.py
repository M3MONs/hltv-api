from flask import Flask, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os, time, json, subprocess

app = Flask(__name__)

limiter = Limiter(app, default_limits=["1 per second"])


def should_run_spider(json_name: str, hours: int = 1):
    localization = f"./hltv_scraper/{json_name}.json"
    if os.path.exists(localization) and time.time() - os.path.getmtime(localization) < (
        3600 * hours
    ):
        return False
    return True


def clear_old_data(json_name: str):
    open(f"./hltv_scraper/{json_name}.json", "w").close()


def run_spider(spider_name: str, json_name: str):
    clear_old_data(json_name)
    process = subprocess.Popen(
        ["scrapy", "crawl", spider_name, "-o", f"{json_name}.json"],
        cwd="./hltv_scraper",
    )
    process.wait()


def run_team_profile_spider(spider_name: str, name: str):
    process = subprocess.Popen(
        [
            "scrapy",
            "crawl",
            spider_name,
            "-a",
            f"team={name}",
        ],
        cwd="./hltv_scraper",
    )
    process.wait()


def run_team_spider(spider_name: str, name: str, profile: str):

    process = subprocess.Popen(
        [
            "scrapy",
            "crawl",
            spider_name,
            "-a",
            f"team={profile}",
            "-o",
            f"{name}.json",
        ],
        cwd="./hltv_scraper",
    )
    process.wait()


@app.route("/results", methods=["GET"])
def results():
    spider_name = "hltv_results"
    json_name = "results"

    if should_run_spider(json_name):
        run_spider(spider_name, json_name)

    with open(f"./hltv_scraper/{json_name}.json", "r") as file:
        data = json.load(file)

    return jsonify(data)


@app.route("/big_results", methods=["GET"])
def big_results():
    spider_name = "hltv_big_results"
    json_name = "big_results"

    if should_run_spider(json_name):
        run_spider(spider_name, json_name)

    with open(f"./hltv_scraper/{json_name}.json", "r") as file:
        data = json.load(file)

    return jsonify(data)


@app.route("/top_teams", methods=["GET"])
def top30():
    spider_name = "hltv_top30"
    json_name = "top_teams"

    if should_run_spider(json_name):
        run_spider(spider_name, json_name)

    with open(f"./hltv_scraper/{json_name}.json", "r") as file:
        data = json.load(file)

    return jsonify(data)


@app.route("/upcoming_matches", methods=["GET"])
def upcoming_matches():
    spider_name = "hltv_upcoming_matches"
    json_name = "upcoming_matches"

    if should_run_spider(json_name):
        run_spider(spider_name, json_name)

    with open(f"./hltv_scraper/{json_name}.json", "r") as file:
        data = json.load(file)

    return jsonify(data)


def is_team_profile_link(team_name: str):
    profiles_json = "./hltv_scraper/teams_profile.json"

    if not os.path.exists(profiles_json):
        return False

    with open(profiles_json) as file:
        profiles = json.load(file)
        if team_name in profiles:
            return True

    return False


def get_profile_link(team_name: str):
    profiles_json = "./hltv_scraper/teams_profile.json"
    with open(profiles_json) as file:
        profiles = json.load(file)
        return profiles[team_name]


@app.route("/team/<name>", methods=["GET"])
@limiter.limit("1 per second")
def team(name: str):
    spider_name = "hltv_teams_id"
    spider_name2 = "hltv_team"

    if not is_team_profile_link(name.lower()):
        run_team_profile_spider(spider_name, name)

    if not is_team_profile_link(name.lower()):
        return "Team not found!"

    profile_link = get_profile_link(name.lower())
    if should_run_spider(name.lower(), 24):
        run_team_spider(spider_name2, name.lower(), profile_link)

    with open(f"./hltv_scraper/{name.lower()}.json", "r") as file:
        data = json.load(file)

    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True, port=8000)
