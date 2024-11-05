from .conditions import Condition, FileTimeCondition, JsonFileEmptyCondition, FileExistsCondition

class ConditionFactory:
    @staticmethod
    def get(condition_type) -> Condition:
        if condition_type == 'file_time':
            return FileTimeCondition()
        elif condition_type == 'json_file_empty':
            return JsonFileEmptyCondition()
        elif condition_type == 'file_exists':
            return FileExistsCondition()
        else:
            raise ValueError(f"Unknown condition type: {condition_type}")