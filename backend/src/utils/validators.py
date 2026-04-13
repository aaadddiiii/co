def require_fields(data, fields):
    for f in fields:
        if f not in data or data[f] in [None, ""]:
            return f"{f} is required"
    return None


def validate_email(email):
    return isinstance(email, str) and "@" in email and "." in email


def validate_positive(value):
    try:
        return float(value) >= 0
    except:
        return False


def validate_int(value):
    try:
        int(value)
        return True
    except:
        return False