from flask import Flask, jsonify
from flask_limiter import Limiter
from utils import (
    should_run_spider,
    run_spider,
    get_profile_link,
    is_team_profile_link,
    is_player_profiles,
)
import json

app = Flask(__name__)

limiter = Limiter(app, default_limits=["1 per second"])


@app.route("/results", methods=["GET"])
def results():
    spider_name = "hltv_results"
    json_name = "results"

    if should_run_spider(json_name):
        run_spider(spider_name, json_name, f"-o {json_name}.json")

    with open(f"./hltv_scraper/{json_name}.json", "r") as file:
        data = json.load(file)

    return jsonify(data)


@app.route("/big_results", methods=["GET"])
def big_results():
    spider_name = "hltv_big_results"
    json_name = "big_results"

    if should_run_spider(json_name):
        run_spider(spider_name, json_name, f"-o {json_name}.json")

    with open(f"./hltv_scraper/{json_name}.json", "r") as file:
        data = json.load(file)

    return jsonify(data)


@app.route("/top_teams", methods=["GET"])
def top30():
    spider_name = "hltv_top30"
    json_name = "top_teams"

    if should_run_spider(json_name):
        run_spider(spider_name, json_name, f"-o {json_name}.json")

    with open(f"./hltv_scraper/{json_name}.json", "r") as file:
        data = json.load(file)

    return jsonify(data)


@app.route("/upcoming_matches", methods=["GET"])
def upcoming_matches():
    spider_name = "hltv_upcoming_matches"
    json_name = "upcoming_matches"

    if should_run_spider(json_name):
        run_spider(spider_name, json_name, f"-o {json_name}.json")

    with open(f"./hltv_scraper/{json_name}.json", "r") as file:
        data = json.load(file)

    return jsonify(data)


@app.route("/team/<name>", methods=["GET"])
@limiter.limit("1 per second")
def team(name: str):
    name = name.lower()
    spider_name = "hltv_teams_id"
    spider_name2 = "hltv_team"

    if not is_team_profile_link(name):
        run_spider(spider_name, name, f"-a team={name}")

    if not is_team_profile_link(name):
        return "Team not found!"

    profile_link = get_profile_link(name)

    if should_run_spider(name, 24):
        run_spider(spider_name2, name, f"-a team={profile_link} -o {name}.json")

    with open(f"./hltv_scraper/{name}.json", "r") as file:
        data = json.load(file)

    return jsonify(data)


@app.route("/player/<name>", methods=["GET"])
@limiter.limit("1 per second")
def player(name: str):
    name = name.lower()
    spider_name = "hltv_players_search"

    if not is_player_profiles(name):
        run_spider(spider_name, name, f"-a player={name}")

    return "In progress..."


if __name__ == "__main__":
    app.run(debug=True, port=8000)
