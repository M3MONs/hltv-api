from .spider_run_condition import SpiderRunCondition


class SpiderRunChecker:
    def __init__(self, conditions: list[SpiderRunCondition]):
        self.conditions = conditions

    def should_run_spider(self, file_path: str, hours: int = 1) -> bool:
        for condition in self.conditions:
            if condition.should_run(file_path, hours):
                return True
        return False
