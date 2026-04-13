from flask import session
from src.db.model import User, Schedule, Teacher
from src.utils import role_required

def routes(app):
    @role_required("teacher")
    @app.route("/schedule/teacher")
    def teacher_schedule():
        user_id = session.get("user_id")

        user = User.query.get(user_id)
        teacher = user.teacher
        if not teacher:
            return error("Unauthorized", 401)

        data = teacher.schedules

        return {
            "schedule": [
                {
                    "day": s.day,
                    "period": s.period,
                    "subject": s.subject,
                    "class_id": s.class_id
                } for s in data
            ]
        }