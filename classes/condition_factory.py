from .spider_run_condition import FileTimeCondition, JsonFileEmptyCondition

class ConditionFactory:
    @staticmethod
    def get(condition_type):
        if condition_type == 'file_time':
            return FileTimeCondition()
        elif condition_type == 'json_file_empty':
            return JsonFileEmptyCondition()
        else:
            raise ValueError(f"Unknown condition type: {condition_type}")