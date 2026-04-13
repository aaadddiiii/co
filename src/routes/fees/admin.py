from flask import request
from src.db.model import db, Fee
from src.utils import role_required


def route(app):

    @app.route("/fees/create", methods=["POST"])
    @role_required("admin")
    def create_fee():
        student_id = int(request.form["student_id"])
        total = float(request.form["total"])

        fee = Fee(
            student_id=student_id,
            total=total,
            paid=0,
            status="due"
        )

        db.session.add(fee)
        db.session.commit()

        return "Fee created"


    @app.route("/fees/all")
    @role_required("admin")
    def all_fees():
        data = Fee.query.all()

        return {
            "fees": [
                {
                    "id": f.id,
                    "student_id": f.student_id,
                    "total": f.total,
                    "paid": f.paid,
                    "status": f.status
                } for f in data
            ]
        }