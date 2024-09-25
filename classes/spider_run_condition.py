import os
import time
import json
from typing import Protocol


class SpiderRunCondition(Protocol):
    def should_run(self, file_path: str, hours: int) -> bool:
        pass


class FileTimeCondition(SpiderRunCondition):
    def should_run(self, file_path: str, hours: int) -> bool:
        if not os.path.exists(file_path):
            return True
        file_age_in_seconds = time.time() - os.path.getmtime(file_path)
        return file_age_in_seconds > (3600 * hours)


class JsonFileEmptyCondition(SpiderRunCondition):
    def should_run(self, file_path: str, hours: int) -> bool:
        if not os.path.exists(file_path):
            return True

        try:
            with open(file_path, "r") as file:
                file_data = json.load(file)
                return file_data == []
        except Exception as e:
            print(f"Error loading JSON file: {e}")
            return True
