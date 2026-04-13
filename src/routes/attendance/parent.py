from flask import session
from src.db.model import Student, StudentAttendance
from src.utils import role_required

def route(app):

    @role_required("parent")
    @app.route("/attendance/parent")
    def parent_view():
        user_id = session.get("user_id")

        students = Student.query.filter_by(parent_id=user_id).all()
        if not student:
            return "Unauthorized", 403

        records = StudentAttendance.query.filter_by(
            student_id=student.id
        ).all()

        result = []

        for s in students:
            records = StudentAttendance.query.filter_by(student_id=s.id).all()

            result.append({
                "student_id": s.id,
                "attendance": [
                    {
                        "date": str(r.date),
                        "period": r.period,
                        "status": r.status
                    } for r in records
                ]
            })

        return {"data": result}