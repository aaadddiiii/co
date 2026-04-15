from flask import session
from src.db.model import User, Schedule, Teacher
from src.utils import role_required, success, error

def routes(app):

    @role_required("teacher")
    @app.route("/schedule/teacher")
    def teacher_schedule():
        user_id = session.get("user_id")

        teacher = Teacher.query.filter_by(user_id=user_id).first()
        if not teacher:
            return error("Unauthorized", 401)

        schedules = Schedule.query.filter_by(teacher_id=teacher.id).all()

        return success(data={
            "schedule": [
                {
                    "id": s.id,
                    "day": s.day,
                    "period": s.period,
                    "subject": s.subject,
                    "class_id": s.class_id
                } for s in schedules
            ]
        })