from flask import request, session
from datetime import date
from src.utils.attendance import is_valid_teaching_time
from src.utils import role_required
from src.db.model import db, Teacher, StudentAttendance, TeacherAttendance, Schedule, Student


def route(app):

    # -------- MARK ATTENDANCE --------
    @role_required("teacher")
    @app.route("/attendance/teacher/mark", methods=["POST"])
    def mark_attendance():
        user_id = session.get("user_id")

        teacher = Teacher.query.filter_by(user_id=user_id).first()
        if not teacher:
            return "Unauthorized", 403

        data = request.get_json()

        class_id = int(data["class_id"])
        period = int(data["period"])
        students = data["students"]  # [{id, status}]

        # ✅ check schedule + time
        if not is_valid_teaching_time(teacher.id, class_id, period):
            return "Not allowed", 403

        today = date.today()

        # ✅ prevent duplicate teacher attendance
        exists = TeacherAttendance.query.filter_by(
            teacher_id=teacher.id,
            date=today,
            period=period
        ).first()

        if exists:
            return "Already marked", 400

        # ✅ mark teacher
        db.session.add(TeacherAttendance(
            teacher_id=teacher.id,
            date=today,
            period=period,
            status="present"
        ))

        # ✅ restrict students to class
        valid_students = Student.query.filter_by(class_id=class_id).all()
        valid_ids = {s.id for s in valid_students}

        for s in students:

            # skip invalid students
            if s["id"] not in valid_ids:
                continue

            # prevent duplicate student attendance
            dup = StudentAttendance.query.filter_by(
                student_id=s["id"],
                date=today,
                period=period
            ).first()

            if dup:
                continue

            db.session.add(StudentAttendance(
                student_id=s["id"],
                class_id=class_id,
                date=today,
                period=period,
                status=s["status"]
            ))

        db.session.commit()
        return "Marked"


    # -------- VIEW OWN ATTENDANCE --------
    @role_required("teacher")
    @app.route("/attendance/teacher/self")
    def teacher_view():
        user_id = session.get("user_id")

        teacher = Teacher.query.filter_by(user_id=user_id).first()
        if not teacher:
            return "Unauthorized", 403

        data = TeacherAttendance.query.filter_by(
            teacher_id=teacher.id
        ).all()

        return {
            "attendance": [
                {"date": str(r.date), "period": r.period, "status": r.status}
                for r in data
            ]
        }



    # -------- VIEW STUDENT ATTENDANCE (OWN CLASSES) --------
    @role_required("teacher")
    @app.route("/attendance/teacher/students")
    def view_students_attendance():
        user_id = session.get("user_id")

        teacher = Teacher.query.filter_by(user_id=user_id).first()
        if not teacher:
            return "Unauthorized", 403

        # get teacher's classes
        schedules = Schedule.query.filter_by(teacher_id=teacher.id).all()
        class_ids = [s.class_id for s in schedules]

        data = StudentAttendance.query.filter(
            StudentAttendance.class_id.in_(class_ids)
        ).all()

        return {
            "attendance": [
                {
                    "student_id": r.student_id,
                    "class_id": r.class_id,
                    "date": str(r.date),
                    "period": r.period,
                    "status": r.status
                } for r in data
            ]
        }


    # -------- EDIT ATTENDANCE (LIMITED CONTROL) --------
    @role_required("teacher")
    @app.route("/attendance/teacher/update", methods=["POST"])
    def teacher_update_attendance():
        user_id = session.get("user_id")

        teacher = Teacher.query.filter_by(user_id=user_id).first()
        if not teacher:
            return "Unauthorized", 403

        record_id = int(request.form["id"])
        status = request.form["status"]

        record = StudentAttendance.query.get(record_id)
        if not record:
            return "Not found", 404

        # ✅ restrict edit to valid time
        if not is_valid_teaching_time(
            teacher.id,
            record.class_id,
            record.period
        ):
            return "Edit window closed", 403

        record.status = status
        db.session.commit()

        return "Updated"