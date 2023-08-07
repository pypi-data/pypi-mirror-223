from typing import Any


def set_key_resolver(instance: dict, key: str, default: Any):
    return instance[key] if instance is not None and key in instance and instance[key] is not None else default
