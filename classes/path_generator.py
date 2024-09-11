from abc import ABC, abstractmethod


class FilePathGenerator(ABC):
    @abstractmethod
    def __init__(self, base_path: str):
        pass

    @abstractmethod
    def generate_path(self, filename: str) -> str:
        pass


class JsonFilePathGenerator(FilePathGenerator):
    def __init__(self, base_path: str):
        self.base_path = base_path

    def generate_path(self, filename: str) -> str:
        return f"{self.base_path}/{filename}.json"
