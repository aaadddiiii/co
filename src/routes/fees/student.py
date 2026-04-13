from flask import session, request, current_app
from werkzeug.utils import secure_filename
import os
import uuid
from src.db.model import db, Student, Fee, Payment, User
from src.utils import role_required



ALLOWED = {"png", "jpg", "jpeg"}



def route(app):

    # -------- VIEW OWN FEES --------
    @role_required("student")
    @app.route("/fees/student")
    def view_fee():
        user_id = session.get("user_id")

        student = Student.query.filter_by(user_id=user_id).first()
        if not student:
            return "Unauthorized", 403

        fees = Fee.query.filter_by(student_id=student.id).all()

        return {
            "fees": [
                {
                    "id": f.id,
                    "total": f.total,
                    "paid": f.paid,
                    "status": f.status
                } for f in fees
            ]
        }


    # -------- PAY (student + parent) --------
    @role_required("student", "parent")
    @app.route("/fees/pay", methods=["POST"])
    def upload_payment():
        user_id = session.get("user_id")

        user = User.query.get(user_id)
        if not user:
            return "Unauthorized", 403

        fee_id = int(request.form["fee_id"])
        amount = float(request.form["amount"])
        txn_id = request.form["txn_id"]


        # -------- identify student --------
        if user.role == "student":
            student = Student.query.filter_by(user_id=user_id).first()

        elif user.role == "parent":
            student_id = int(request.form["student_id"])
            student = Student.query.filter_by(
                id=student_id,
                parent_id=user_id
            ).first()
        else:
            return "Forbidden", 403

        if not student:
            return "Invalid student", 403

        fee = Fee.query.get(fee_id)
        if not fee or fee.student_id != student.id:
            return "Invalid fee", 400


        # -------- file upload --------
        file = request.files.get("screenshot")
        filename = None
        if file:
            ext = file.filename.split(".")[-1].lower()

            if ext not in {"png", "jpg", "jpeg"}:
                return "Invalid file type", 400

            filename = f"{uuid.uuid4()}.{ext}"

            upload_folder = current_app.config["UPLOAD_FOLDER"]
            filepath = os.path.join(upload_folder, secure_filename(filename))

            file.save(filepath)


        # -------- save payment --------
        payment = Payment(
            student_id=student.id,
            fee_id=fee.id,
            amount=amount,
            txn_id=txn_id,
            screenshot=filename,
            status="pending"
        )

        db.session.add(payment)
        db.session.commit()

        return "Payment submitted"