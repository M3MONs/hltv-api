from flask import Flask, jsonify
import os, time, json, subprocess

app = Flask(__name__)


def should_run_spider(json_name: str):
    localization = f"./hltv_scraper/{json_name}.json"
    if os.path.exists(localization) and os.path.getsize(localization) > 0:
        return False
    if (
        os.path.exists(localization)
        and time.time() - os.path.getmtime(localization) < 3600
    ):
        return False
    return True


def run_spider(spider_name: str, json_name: str):
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

    with open("./hltv_scraper/results.json", "r") as file:
        data = json.load(file)

    return jsonify({"data": data})


if __name__ == "__main__":
    app.run(debug=True, port=8000)
