from flask import request
from src.db.model import db, Fee
from src.utils import role_required
from src.utils.request_utils import get_int, get_float, get_str


def routes(app):

    @app.route("/fees/create", methods=["POST"])
    @role_required("admin")
    def create_fee():

        data = request.form

        student_id, err = get_int(data, "student_id")
        if err: return err

        total, err = get_float(data, "total")
        if err: return err

        fee = Fee(
            student_id=student_id,
            total=total,
            paid=0,
            status="due"
        )

        db.session.add(fee)
        db.session.commit()

        return success(message="Fee created")


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