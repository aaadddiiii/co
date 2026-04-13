from flask import session
from src.db.model import Student, StudentAttendance
from src.utils import role_required


def route(app):
    
    @role_required("student")
    @app.route("/attendance/student")
    def student_view():
        user_id = session.get("user_id")

        student = Student.query.filter_by(user_id=user_id).first()
        if not student:
            return "Unauthorized", 403

        records = StudentAttendance.query.filter_by(
            student_id=student.id
        ).all()

        return {
            "attendance": [
                {
                    "date": str(r.date),
                    "period": r.period,
                    "status": r.status
                } for r in records
            ]
        }