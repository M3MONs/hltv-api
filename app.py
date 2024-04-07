import datetime
from flask import Flask, jsonify
from flask_limiter import Limiter
from utils import (
    should_run_spider,
    run_spider,
    run_spider_and_get_data,
    get_profile_data,
    load_json_data,
    is_profile_link,
)

app = Flask(__name__)

limiter = Limiter(app, default_limits=["1 per second"])


@app.route("/results", methods=["GET"])
def results():
    spider_name = "hltv_results"
    json_name = "results"

    data = run_spider_and_get_data(spider_name, json_name, f"-o {json_name}.json")

    return jsonify(data)


@app.route("/big_results", methods=["GET"])
def big_results():
    spider_name = "hltv_big_results"
    json_name = "big_results"

    data = run_spider_and_get_data(spider_name, json_name, f"-o {json_name}.json")

    return jsonify(data)


@app.route("/top_teams", methods=["GET"])
def top30():
    spider_name = "hltv_top30"
    json_name = "top_teams"

    data = run_spider_and_get_data(spider_name, json_name, f"-o {json_name}.json")

    return jsonify(data)


@app.route("/upcoming_matches", methods=["GET"])
def upcoming_matches():
    spider_name = "hltv_upcoming_matches"
    json_name = "upcoming_matches"

    data = run_spider_and_get_data(spider_name, json_name, f"-o {json_name}.json")

    return jsonify(data)


today = datetime.date.today()


@app.route("/news", defaults={"year": today.year, "month": today.strftime("%B")})
@app.route("/news/<year>/<month>")
@limiter.limit("1 per second")
def news(year: str, month: str):
    spider_name = "hltv_news"
    filename = f"news_{year}_{month}"

    print(should_run_spider(filename))

    data = run_spider_and_get_data(
        spider_name, filename, f"-a year={year} -a month={month} -o {filename}.json"
    )

    return jsonify(data)


@app.route("/team/<name>", methods=["GET"])
@limiter.limit("1 per second")
def team(name: str):
    name = name.lower()
    spider_name = "hltv_teams_id"
    spider_name2 = "hltv_team"

    if not is_profile_link("teams_profile", name):
        run_spider(spider_name, name, f"-a team={name}")

    if not is_profile_link("teams_profile", name):
        return "Team not found!"

    profile_link = get_profile_data("teams_profile", name)

    if should_run_spider(name, 24):
        run_spider(spider_name2, name, f"-a team={profile_link} -o {name}.json")

    data = load_json_data(name)

    return jsonify(data)


@app.route("/profile/team/<id>/<team>", methods=["GET"])
@limiter.limit("1 per second")
def team(id: str, team: str):
    filename = team

    return f"{id}/{filename}"


@app.route("/player/<name>", methods=["GET"])
@limiter.limit("1 per second")
def player(name: str):
    name = name.lower()
    spider_name = "hltv_players_search"

    if not is_profile_link("players_profiles", name):
        run_spider(spider_name, name, f"-a player={name}")

    if not is_profile_link("players_profiles", name):
        return "Player not found!"

    profiles = get_profile_data("players_profiles", name)

    return jsonify(profiles)


@app.route("/profile/player/<id>/<player>", methods=["GET"])
@limiter.limit("1 per second")
def player_profile(id: str, player: str):
    spider_name = "hltv_player"
    filename = player
    data = run_spider_and_get_data(
        spider_name, filename, f"-a profile=/player/{id}/{player} -o {filename}.json"
    )
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True, port=8000)
