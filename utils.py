import os, time, subprocess, json

BASE_DIR = "./hltv_scraper"


def should_run_spider(json_name: str, hours: int = 1) -> bool:
    localization = os.path.join(BASE_DIR, f"{json_name}.json")
    if os.path.exists(localization) and time.time() - os.path.getmtime(localization) < (
        3600 * hours
    ):
        return False
    return True


def load_json_data(filename: str) -> dict:
    with open(f"./hltv_scraper/{filename}.json", "r") as file:
        return json.load(file)


def is_profile_link(filename: str, profile: str) -> bool:
    file = os.path.join(BASE_DIR, f"{filename}.json")

    if not os.path.exists(file):
        return False

    with open(file) as f:
        profiles = json.load(f)
        if profile in profiles:
            return True

    return False


def get_profile_data(filename: str, profile: str) -> dict:
    file = os.path.join(BASE_DIR, f"{filename}.json")
    with open(file) as f:
        profiles = json.load(f)
        return profiles[profile]


def clear_old_data(json_name: str) -> None:
    open(os.path.join(BASE_DIR, f"{json_name}.json"), "w").close()


def run_spider(spider_name: str, json_name: str, args: str) -> None:
    if os.path.exists(os.path.join(BASE_DIR, f"{json_name}.json")):
        clear_old_data(json_name)

    process = subprocess.Popen(
        ["scrapy", "crawl", spider_name] + args.split(),
        cwd=BASE_DIR,
    )
    process.wait()


def run_spider_and_get_data(spider: str, filename: str, spider_args: str) -> dict:
    if should_run_spider(filename):
        run_spider(spider, filename, spider_args)
    return load_json_data(filename)
