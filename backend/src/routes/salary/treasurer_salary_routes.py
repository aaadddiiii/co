from src.db.model import TeacherPayment, db
from src.utils import role_required
from src.utils.response import success, error
from src.utils.request_utils import get_int, get_float, get_str



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

        data = request.form

        payment_id, err = get_int(data, "payment_id")
        if err: return err

        payment = TeacherPayment.query.get(payment_id)
        if not payment:
            return error("Not found", 404)
        
        if payment.status == "paid":
            return error("Already paid", 400)

        if payment.status != "approved":
            return error("Not approved yet", 400)

        payment.status = "paid"

        from src.db.model import AccountLog

        db.session.add(AccountLog(
            type="debit",
            amount=payment.amount,
            description=f"Salary paid to teacher {payment.teacher_id}",
            reference_id=payment.id
        ))

        db.session.commit()

        return success(message="Salary paid")