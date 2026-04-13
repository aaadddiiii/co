from flask import request
from datetime import time
from src.db.model import db, Schedule
from src.utils import role_required
from src.utils.response import success, error
from src.utils.request_utils import get_int, get_float, get_str


def routes(app):

    # -------- CREATE --------
    @app.route("/schedule/create", methods=["POST"])
    @role_required("admin")
    def create_schedule():
        data = request.form

        day, err = get_str(data, "day")
        if err: return err

        subject, err = get_str(data, "subject")
        if err: return err

        period, err = get_int(data, "period")
        if err: return err

        teacher_id, err = get_int(data, "teacher_id")
        if err: return err

        class_id, err = get_int(data, "class_id")
        if err: return err

        start_raw, err = get_str(data, "start_time")
        if err: return err

        end_raw, err = get_str(data, "end_time")
        if err: return err

        try:
            start_time = time.fromisoformat(start_raw)
            end_time = time.fromisoformat(end_raw)
        except:
            return error("Invalid time format")

        # -------- CONFLICT CHECK --------
        existing = Schedule.query.filter_by(
            day=day, period=period, class_id=class_id
        ).first()

        if existing:
            return error("Schedule exists")

        teacher_conflict = Schedule.query.filter_by(
            day=day,
            period=period,
            teacher_id=teacher_id
        ).first()

        if teacher_conflict:
            return error("Teacher already assigned")

        s = Schedule(
            day=day,
            period=period,
            subject=subject,
            teacher_id=teacher_id,
            class_id=class_id,
            start_time=start_time,
            end_time=end_time
        )

        try:
            db.session.add(s)
            db.session.commit()
        except Exception:
            db.session.rollback()
            return error("Database error", 500)

        return success(message="Created")

    # -------- UPDATE --------
    @app.route("/schedule/update", methods=["POST"])
    @role_required("admin")
    def update_schedule():
        data = request.form

        id, err = get_int(data, "id")
        if err: return err

        s = Schedule.query.get(id)
        if not s:
            return error("Not found", 404)

        day, err = get_str(data, "day")
        if err: return err

        subject, err = get_str(data, "subject")
        if err: return err

        period, err = get_int(data, "period")
        if err: return err

        teacher_id, err = get_int(data, "teacher_id")
        if err: return err

        s.day = day
        s.period = period
        s.subject = subject
        s.teacher_id = teacher_id

        # -------- CONFLICT CHECK --------
        conflict = Schedule.query.filter(
            Schedule.id != s.id,
            Schedule.day == s.day,
            Schedule.period == s.period,
            Schedule.class_id == s.class_id
        ).first()

        if conflict:
            return error("Class conflict")

        teacher_conflict = Schedule.query.filter(
            Schedule.id != s.id,
            Schedule.day == s.day,
            Schedule.period == s.period,
            Schedule.teacher_id == s.teacher_id
        ).first()

        if teacher_conflict:
            return error("Teacher conflict")

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            return error("Database error", 500)

        return success(message="Updated")

    # -------- DELETE --------
    @app.route("/schedule/delete", methods=["POST"])
    @role_required("admin")
    def delete_schedule():
        data = request.form

        id, err = get_int(data, "id")
        if err: return err

        s = Schedule.query.get(id)
        if not s:
            return error("Not found", 404)

        try:
            db.session.delete(s)
            db.session.commit()
        except Exception:
            db.session.rollback()
            return error("Database error", 500)

        return success(message="Deleted")

    # -------- ALL --------
    @app.route("/schedule/all")
    @role_required("admin")
    def all_schedule():
        data = Schedule.query.all()

        result = [
            {
                "id": s.id,
                "day": s.day,
                "period": s.period,
                "subject": s.subject,
                "teacher_id": s.teacher_id,
                "class_id": s.class_id
            } for s in data
        ]

        return success(data=result)