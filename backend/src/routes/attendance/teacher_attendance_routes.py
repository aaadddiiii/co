from flask import request, session
from datetime import date
from src.utils.attendance_utils import is_valid_teaching_time
from src.utils import role_required
from src.utils.response import success
from src.db.model import db, User, Teacher, StudentAttendance, TeacherAttendance, Schedule, Student
from src.utils.request_utils import get_int, get_str


TEST_MODE = True

def routes(app):

    # -------- MARK ATTENDANCE --------
    @app.route("/attendance/teacher/mark", methods=["POST"])
    @role_required("teacher")
    def mark_attendance():

        user_id = session.get("user_id")

        teacher = Teacher.query.filter_by(user_id=user_id).first()
        if not teacher:
            return error("Unauthorized", 401)

        data = request.get_json()

        if not data:
            return error("Invalid JSON", 400)

        class_id, err = get_int(data, "class_id")
        if err: return err

        period, err = get_int(data, "period")
        if err: return err
        students = data.get("students", [])

        # ✅ VALIDATION (with test bypass)
        if not is_valid_teaching_time(teacher.id, class_id, period):
            if not TEST_MODE:
                return error("Not allowed", 403)
            else:
                print("⚠️ TEST MODE: bypassing schedule validation")

        today = date.today()

        # ✅ prevent duplicate teacher attendance
        exists = TeacherAttendance.query.filter_by(
            teacher_id=teacher.id,
            date=today,
            period=period
        ).first()

        if exists:
            return error("Already marked", 400)

        # ✅ mark teacher attendance
        db.session.add(TeacherAttendance(
        teacher_id=teacher.id,
        date=today,
        period=period,
        status="present"
        ))

        # ✅ student attendance (optional)
        valid_students = Student.query.filter_by(class_id=class_id).all()
        valid_ids = {s.id for s in valid_students}

        for s in students:

            if s.get("id") not in valid_ids:
                continue

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
                status=s.get("status", "present")
            ))

        db.session.commit()

        return success(message="Marked")


        

    # -------- VIEW OWN ATTENDANCE --------
    @role_required("teacher")
    @app.route("/attendance/teacher/self")
    def teacher_view():
        user_id = session.get("user_id")

        teacher = Teacher.query.filter_by(user_id=user_id).first()
        if not teacher:
            return error("Unauthorized", 401)

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
            return error("Unauthorized", 401)

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
            return error("Unauthorized", 401)

        data = request.form

        record_id, err = get_int(data, "id")
        if err: return err

        status, err = get_str(data, "status")
        if err: return err

        record = StudentAttendance.query.get(record_id)
        if not record:
            return error("Not found", 404)

        # ensure teacher owns class
        schedules = Schedule.query.filter_by(teacher_id=teacher.id).all()
        allowed_classes = {s.class_id for s in schedules}

        if record.class_id not in allowed_classes:
            return error("Forbidden", 403)


        # ✅ restrict edit to valid time
        if not is_valid_teaching_time(
            teacher.id,
            record.class_id,
            record.period
        ):
            return error("Edit window closed", 403)

        record.status = status
        db.session.commit()

        return success(message="Updated")