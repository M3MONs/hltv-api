from abc import ABC, abstractmethod
import json


class DataLoader(ABC):
    @abstractmethod
    def load(self, file: str) -> dict:
        pass


class JsonDataLoader(DataLoader):
    def load(self, file: str) -> dict:
        try:
            with open(file, "r") as json_file:
                return json.load(json_file)
        except Exception as e:
            raise ValueError(f"Error loading JSON file: {e}")
