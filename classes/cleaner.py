from abc import ABC


class OldDataCleaner(ABC):
    @staticmethod
    def clean():
        pass


class JsonOldDataCleaner(OldDataCleaner):
    @staticmethod
    def clean(file: str) -> None:
        open(file, "w").close()
