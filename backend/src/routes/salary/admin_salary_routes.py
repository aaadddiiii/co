from src.db.model import TeacherPayment, db
from flask import request
from src.utils import role_required
from src.utils.request_utils import get_int, get_float, get_str


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
    
    @app.route("/salary/approve", methods=["POST"])
    @role_required("admin")
    def approve_salary():

        data = request.form

        payment_id, err = get_int(data, "payment_id")
        if err: return err

        payment = TeacherPayment.query.get(payment_id)
        if not payment:
            return error("Not found", 404)

        if payment.status != "pending":
            return error("Invalid state", 400)

        payment.status = "approved"
        db.session.commit()

        return success(message="Approved")