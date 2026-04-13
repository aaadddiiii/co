from flask import session
from src.db.model import Schedule, Teacher
from src.utils import role_required

def route(app):
    @role_required("teacher")
    @app.route("/schedule/teacher")
    def teacher_schedule():
        user_id = session.get("user_id")

        teacher = Teacher.query.filter_by(user_id=user_id).first()
        if not teacher:
            return "Unauthorized", 403

        data = Schedule.query.filter_by(teacher_id=teacher.id).all()

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