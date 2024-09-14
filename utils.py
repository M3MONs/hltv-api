import os, time, subprocess, json

from classes.data import JsonDataLoader as JDL
from classes.path_generator import JsonFilePathGenerator as JFG
from classes.cleaner import JsonOldDataCleaner

BASE_DIR = "./hltv_scraper"
json_path = JFG(BASE_DIR)


def should_run_spider(json_name: str, hours: int = 1) -> bool:
    localization = json_path.generate(json_name)

    if not os.path.exists(localization):
        return True

    if not time.time() - os.path.getmtime(localization) < (3600 * hours):
        return True

    try:
        with open(localization, "r") as file:
            file_data = json.load(file)
            if file_data == []:
                return True
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return True

    return False


def is_profile_link(filename: str, profile: str) -> bool:
    file = json_path.generate(filename)

    if not os.path.exists(file):
        return False

    with open(file) as f:
        profiles = json.load(f)
        if profile in profiles:
            return True

    return False


def get_profile_data(filename: str, profile: str) -> dict:
    file = json_path.generate(filename)
    with open(file) as f:
        profiles = json.load(f)
        return profiles[profile]


def run_spider(spider_name: str, json_name: str, args: str) -> None:
    path = json_path.generate(json_name)
    if os.path.exists(path):
        JsonOldDataCleaner.clean(path)

    process = subprocess.Popen(
        ["scrapy", "crawl", spider_name] + args.split(),
        cwd=BASE_DIR,
    )
    process.wait()


def run_spider_and_get_data(spider: str, filename: str, spider_args: str) -> dict:
    json_loader = JDL()
    if should_run_spider(filename):
        run_spider(spider, filename, spider_args)
    return json_loader.load(json_path.generate(filename))
