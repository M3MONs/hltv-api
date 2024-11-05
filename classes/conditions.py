import os
import time
import json
from abc import ABC, abstractmethod


class Condition(ABC):
    @abstractmethod
    def check(self, file_path: str, hours: int) -> bool:
        pass


class FileTimeCondition(Condition):
    def check(self, file_path: str, hours: int) -> bool:
        if not os.path.exists(file_path):
            return True
        file_age_in_seconds = time.time() - os.path.getmtime(file_path)
        return file_age_in_seconds > (3600 * hours)


class JsonFileEmptyCondition(Condition):
    def check(self, file_path: str, hours: int) -> bool:
        if not os.path.exists(file_path):
            return True

        try:
            with open(file_path, "r") as file:
                file_data = json.load(file)
                return file_data == []
        except Exception as e:
            print(f"Error loading JSON file: {e}")
            return True
