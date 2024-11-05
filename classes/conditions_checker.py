from .conditions import Condition
from abc import ABC, abstractmethod


class Checker(ABC):
    @abstractmethod
    def __init__(self, conditions: list[Condition]):
        pass
    
    @abstractmethod
    def check(self, file_path: str, hours: int = 1) -> bool:
        pass

class ConditionsChecker(Checker):
    def __init__(self, conditions: list[Condition]):
        self.conditions = conditions

    def check(self, file_path: str, hours: int = 1) -> bool:
        for condition in self.conditions:
            if condition.check(file_path, hours):
                return True
        return False
