import os, time, subprocess


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
    clear_old_data(name)
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
