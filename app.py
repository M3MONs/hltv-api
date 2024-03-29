from flask import Flask, jsonify
import os, time, json, subprocess

app = Flask(__name__)


def should_run_spider(json_name: str):
    localization = f"./hltv_scraper/{json_name}.json"
    if (
        os.path.exists(localization)
        and time.time() - os.path.getmtime(localization) < 3600
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


@app.route("/results", methods=["GET"])
def results():
    spider_name = "hltv_results"
    json_name = "results"

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


if __name__ == "__main__":
    app.run(debug=True, port=8000)
