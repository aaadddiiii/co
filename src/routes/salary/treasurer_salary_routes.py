from src.db.model import TeacherPayment, db
from src.utils import role_required


def routes(app):

    @app.route("/salary/all")
    @role_required("treasurer")
    def get_all_salaries():
        data = TeacherPayment.query.order_by(TeacherPayment.year.desc()).all()

        return {
            "salaries": [
                {
                    "id": p.id,
                    "teacher_id": p.teacher_id,
                    "month": p.month,
                    "amount": p.amount,
                    "status": p.status
                } for p in data
            ]
        }


    @app.route("/salary/pay", methods=["POST"])
    @role_required("treasurer")
    def pay_salary():
        from flask import request

        payment_id = int(request.form["payment_id"])

        payment = TeacherPayment.query.get(payment_id)
        if not payment:
            return "Not found", 404

        if payment.status == "paid":
            return "Already paid", 400

        payment.status = "paid"
        db.session.commit()

        return "Salary paid"