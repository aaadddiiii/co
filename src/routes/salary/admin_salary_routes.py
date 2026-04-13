from src.db.model import TeacherPayment
from src.utils import role_required


def routes(app):

    @app.route("/salary/admin")
    @role_required("admin")
    def admin_salary_view():
        data = TeacherPayment.query.order_by(TeacherPayment.year.desc()).all()

        return {
            "salaries": [
                {
                    "teacher_id": p.teacher_id,
                    "month": p.month,
                    "amount": p.amount,
                    "status": p.status
                } for p in data
            ]
        }