from flask import session
from src.db.model import Student, Fee
from src.utils import role_required


def route(app):

    @role_required("student", "parent")
    @app.route("/fees/parent")
    def parent_fee_view():
        user_id = session.get("user_id")

        students = Student.query.filter_by(parent_id=user_id).all()
        if not students:
            return "Unauthorized", 403

        result = []

        for s in students:
            fees = Fee.query.filter_by(student_id=s.id).all()

            result.append({
                "student_id": s.id,
                "fees": [
                    {
                        "id": f.id,
                        "total": f.total,
                        "paid": f.paid,
                        "status": f.status
                    } for f in fees
                ]
            })

        return {"data": result}