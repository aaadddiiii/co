from flask import request
from src.db.model import db, User, Payment, Fee, AccountLog
from src.utils import role_required
from src.utils.request_utils import get_int, get_float, get_str


def routes(app):

    @app.route("/fees/payments")
    @role_required("treasurer")
    def view_payments():
        data = Payment.query.all()

        return {
            "payments": [
                {
                    "id": p.id,
                    "student_id": p.student_id,
                    "amount": p.amount,
                    "txn_id": p.txn_id,
                    "screenshot": p.screenshot,
                    "status": p.status
                } for p in data
            ]
        }


    @app.route("/fees/verify", methods=["POST"])
    @role_required("treasurer")
    def verify_payment():

        data = request.form

        payment_id, err = get_int(data, "payment_id")
        if err: return err

        payment = Payment.query.get(payment_id)
        if not payment:
            return error("Not found", 404)

        if payment.status == "verified":
            return error("Already verified", 400)

        payment.status = "verified"

        fee = payment.fee
        if not fee:
            return error("Fee not found", 404)

        fee.paid += payment.amount

        if fee.paid >= fee.total:
            fee.status = "paid"

        db.session.add(AccountLog(
            type="credit",
            amount=payment.amount,
            description=f"Fee payment by student {payment.student_id}",
            reference_id=payment.id
        ))
        
        db.session.commit()

        return success(message="Verified")