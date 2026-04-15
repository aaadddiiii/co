from flask import request
from src.db.model import db, User, Payment, Fee, AccountLog
from src.utils import role_required, error, success, get_int, get_float, get_str


def routes(app):

    @app.route("/fees/payments")
    @role_required("admin", "treasurer")
    def view_payments():
        data = Payment.query.all()

        return success(data={
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
        
        )


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


    @app.route("/fees/payment/<int:payment_id>")
    @role_required("treasurer")
    def get_payment_detail(payment_id):
        payment = Payment.query.get(payment_id)

        if not payment:
            return error("Payment not found", 404)

        fee = payment.fee

        return success(data={
            "id": payment.id,
            "student_id": payment.student_id,
            "amount": payment.amount,
            "txn_id": payment.txn_id,
            "screenshot": payment.screenshot,
            "status": payment.status,
            "fee": {
                "id": fee.id,
                "total": fee.total,
                "paid": fee.paid,
                "status": fee.status
            } if fee else None
        })