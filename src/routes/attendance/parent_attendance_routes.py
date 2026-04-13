from flask import session
from src.db.model import Student, StudentAttendance
from src.utils import role_required

def routes(app):

    @role_required("parent")
    @app.route("/attendance/parent")
    def parent_view():
        user_id = session.get("user_id")

        user = User.query.get(user_id)
        students = user.children
        if not students:
            return "Unauthorized", 403

        records = StudentAttendance.query.filter_by(
            student_id=student.id
        ).all()

        result = []

        for student in students:
            records = StudentAttendance.query.filter_by(student_id=student.id).all()

            result.append({
                "student_id": student.id,
                "attendance": [
                    {
                        "date": str(r.date),
                        "period": r.period,
                        "status": r.status
                    } for r in records
                ]
            })

        return {"data": result}