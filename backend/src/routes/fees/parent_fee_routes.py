from flask import session
from src.db.model import User, Student, Fee
from src.utils import role_required, success, error


def routes(app):

    @role_required("student", "parent")
    @app.route("/fees/parent")
    def parent_fee_view():
        user_id = session.get("user_id")

        user = User.query.get(user_id)
        students = user.children
        if not students:
            return error("Unauthorized", 401)

        result = []

        for student in students:
            fees = Fee.query.filter_by(student_id=student.id).all()

            result.append({
                "student_id": student.id,
                "fees": [
                    {
                        "id": f.id,
                        "total": f.total,
                        "paid": f.paid,
                        "status": f.status
                    } for f in fees
                ]
            })

        return success(data={"data": result})