from flask import session
from src.db.model import Schedule, Student
from src.utils import role_required, error, success

def routes(app):
    @role_required("student")
    @app.route("/schedule/student")
    def student_schedule():
        user_id = session.get("user_id")

        student = Student.query.filter_by(user_id=user_id).first()
        if not student:
            return error("Unauthorized", 401)

        data = Schedule.query.filter_by(class_id=student.class_id).all()

        return success(data={
            "schedule": [
                {
                    "day": s.day,
                    "period": s.period,
                    "subject": s.subject,
                    "teacher_id": s.teacher_id
                } for s in data
            ]
        })