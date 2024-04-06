from typing import Any
import scrapy
import datetime
from .utils import parse_news

today = datetime.date.today()


class HltvNewsSpider(scrapy.Spider):
    name = "hltv_news"
    allowed_domains = ["www.hltv.org"]

    def __init__(self, year: str, month: str, **kwargs: Any):
        self.date = f"{year}/{month}"
        self.start_urls = [f"https://www.hltv.org/news/archive/{self.date}"]
        super().__init__(**kwargs)

    def parse(self, response):
        articles = response.css(".article")
        data = parse_news(articles)
        yield {"news": data}
