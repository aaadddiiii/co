from flask import request
from src.db.model import db, Payment, Fee
from src.utils import role_required


def route(app):

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
        payment_id = int(request.form["payment_id"])

        payment = Payment.query.get(payment_id)
        if not payment:
            return "Not found", 404

        if payment.status == "verified":
            return "Already verified", 400

        payment.status = "verified"

        fee = Fee.query.get(payment.fee_id)
        if not fee:
            return "Fee not found", 404

        fee.paid += payment.amount

        if fee.paid >= fee.total:
            fee.status = "paid"

        db.session.commit()

        return "Verified"