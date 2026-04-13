from functools import wraps
from flask import session
from src.db.model import User, Teacher


def role_required(*allowed_roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user_id = session.get("user_id")

            if not user_id:
                return error("Unauthorized", 401)

            user = User.query.get(user_id)

            if user.role not in allowed_roles:
                return error("Forbidden", 403)

            return f(*args, **kwargs)
        return wrapper
    return decorator


def can_create_user(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        user_id = session.get("user_id")

        if not user_id:
            return error("Unauthorized", 401)

        user = User.query.get(user_id)

        if user.role == "admin":
            return f(*args, **kwargs)

        if user.role == "teacher":
            teacher = Teacher.query.filter_by(user_id=user.id).first()
            if teacher and teacher.type == "permanent":
                return f(*args, **kwargs)

        return error("Forbidden", 403)
    return wrapper