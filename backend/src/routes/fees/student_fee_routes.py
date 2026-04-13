from flask import session, request, current_app
from werkzeug.utils import secure_filename
import os
import uuid
import imghdr
from src.db.model import db, User, Student, Fee, Payment, User
from src.utils import role_required
from src.utils.response import error
from src.utils.request_utils import get_int, get_float, get_str




ALLOWED = {"png", "jpg", "jpeg"}



def routes(app):

    # -------- VIEW OWN FEES --------
    @role_required("student")
    @app.route("/fees/student")
    def view_fee():
        user_id = session.get("user_id")

        user = User.query.get(user_id)
        student = user.student
        if not student:
            return error("Unauthorized", 401)

        fees = student.fees

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
            return error("Unauthorized", 401)
        data = request.form

        fee_id, err = get_int(data, "fee_id")
        if err: return err

        amount, err = get_float(data, "amount")
        if err: return err

        txn_id, err = get_str(data, "txn_id")
        if err: return err

        student_id, err = get_int(data, "student_id")
        if err: return err


        # -------- identify student --------
        if user.role == "student":
            student = Student.query.filter_by(user_id=user_id).first()

        elif user.role == "parent":
            student_id, err = get_int(data, "student_id")
            if err: return err
            student = Student.query.filter_by(
                id=student_id,
                parent_id=user_id
            ).first()
        else:
            return error("Forbidden", 403)

        if not student:
            return error("Invalid student", 403)

        fee = Fee.query.get(fee_id)
        if not fee or fee.student_id != student.id:
            return error("Invalid fee", 400)


        # -------- file upload --------
        file = request.files.get("screenshot")
        filename = None

        if file:
            ext = file.filename.split(".")[-1].lower()

            if ext not in {"png", "jpg", "jpeg"}:
                return error("Invalid file type")

            # size check
            file.seek(0, 2)
            size = file.tell()
            file.seek(0)

            if size > 2 * 1024 * 1024:
                return error("File too large")

            # MIME check
            header = file.read(512)
            file.seek(0)

            if imghdr.what(None, header) not in {"png", "jpeg"}:
                return error("Invalid image content")

            filename = f"{uuid.uuid4()}.{ext}"

            upload_folder = current_app.config["UPLOAD_FOLDER"]
            os.makedirs(upload_folder, exist_ok=True)

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

        return success(message="Payment submitted")