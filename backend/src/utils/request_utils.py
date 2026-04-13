from src.utils.validators import validate_int, validate_positive
from src.utils.response import error


def get_int(data, key):
    if key not in data:
        return None, error(f"{key} is required")
    if not validate_int(data[key]):
        return None, error(f"{key} must be integer")
    return int(data[key]), None


def get_float(data, key):
    if key not in data:
        return None, error(f"{key} is required")
    if not validate_positive(data[key]):
        return None, error(f"{key} must be positive number")
    return float(data[key]), None


def get_str(data, key):
    if key not in data or not str(data[key]).strip():
        return None, error(f"{key} is required")
    return str(data[key]).strip(), None