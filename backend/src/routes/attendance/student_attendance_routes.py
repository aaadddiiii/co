from flask import session
from src.db.model import User, Student, StudentAttendance
from src.utils import role_required


def routes(app):
    
    @role_required("student")
    @app.route("/attendance/student")
    def student_view():
        user_id = session.get("user_id")

        user = User.query.get(user_id)
        student = user.student
        if not student:
            return error("Unauthorized", 401)

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