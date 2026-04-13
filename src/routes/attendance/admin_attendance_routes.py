from flask import request
from datetime import date
from src.db.model import db, StudentAttendance, TeacherAttendance
from src.utils import role_required


def routes(app):

    # -------- VIEW ALL STUDENT ATTENDANCE --------
    @app.route("/attendance/admin/students")
    @role_required("admin")
    def view_all_student_attendance():
        records = StudentAttendance.query.all()

        return {
            "attendance": [
                {
                    "student_id": r.student_id,
                    "class_id": r.class_id,
                    "date": str(r.date),
                    "period": r.period,
                    "status": r.status
                } for r in records
            ]
        }


    # -------- VIEW ALL TEACHER ATTENDANCE --------
    @app.route("/attendance/admin/teachers")
    @role_required("admin")
    def view_all_teacher_attendance():
        records = TeacherAttendance.query.all()

        return {
            "attendance": [
                {
                    "teacher_id": r.teacher_id,
                    "date": str(r.date),
                    "period": r.period,
                    "status": r.status
                } for r in records
            ]
        }


    # -------- FILTER ATTENDANCE --------
    @app.route("/attendance/admin/filter")
    @role_required("admin")
    def filter_attendance():
        student_id = request.args.get("student_id")
        teacher_id = request.args.get("teacher_id")
        date_q = request.args.get("date")

        if student_id:
            q = StudentAttendance.query.filter_by(student_id=student_id)
        elif teacher_id:
            q = TeacherAttendance.query.filter_by(teacher_id=teacher_id)
        else:
            return "Provide filter", 400

        if date_q:
            q = q.filter_by(date=date.fromisoformat(date_q))

        data = q.all()

        return {"data": [
            {
                "id": r.id,
                "date": str(r.date),
                "period": r.period,
                "status": r.status
            } for r in data
        ]}


    # -------- UPDATE ATTENDANCE --------
    @app.route("/attendance/admin/update", methods=["POST"])
    @role_required("admin")
    def admin_update_attendance():
        id = int(request.form["id"])
        type_ = request.form["type"]  # student / teacher
        status = request.form["status"]

        if type_ == "student":
            record = StudentAttendance.query.get(id)
        else:
            record = TeacherAttendance.query.get(id)

        if not record:
            return "Not found", 404

        record.status = status
        db.session.commit()

        return "Updated"


    # -------- DELETE ATTENDANCE --------
    @app.route("/attendance/admin/delete", methods=["POST"])
    @role_required("admin")
    def delete_attendance():
        id = int(request.form["id"])
        type_ = request.form["type"]

        if type_ == "student":
            record = StudentAttendance.query.get(id)
        else:
            record = TeacherAttendance.query.get(id)

        if not record:
            return "Not found", 404

        db.session.delete(record)
        db.session.commit()

        return "Deleted"


    # -------- MANUAL MARK ABSENT (TEACHER) --------
    @app.route("/attendance/admin/mark-absent", methods=["POST"])
    @role_required("admin")
    def mark_teacher_absent():
        teacher_id = int(request.form["teacher_id"])
        period = int(request.form["period"])
        today = date.today()

        exists = TeacherAttendance.query.filter_by(
            teacher_id=teacher_id,
            date=today,
            period=period
        ).first()

        if not exists:
            db.session.add(TeacherAttendance(
                teacher_id=teacher_id,
                date=today,
                period=period,
                status="absent"
            ))
            db.session.commit()

        return "Marked"