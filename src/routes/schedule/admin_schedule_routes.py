from flask import request
from src.db.model import db, Schedule
from src.utils import role_required
from datetime import time

def routes(app):
    @app.route("/schedule/create", methods=["POST"])
    @role_required("admin")
    def create_schedule():
        day = request.form["day"]
        period = int(request.form["period"])
        subject = request.form["subject"]
        teacher_id = int(request.form["teacher_id"])
        class_id = int(request.form["class_id"])
        start_time = request.form["start_time"]  # "10:00"
        end_time = request.form["end_time"]

        start_time = time.fromisoformat(start_time)
        end_time = time.fromisoformat(end_time)

        existing = Schedule.query.filter_by(
            day=day, period=period, class_id=class_id
        ).first()

        if existing:
            return "Schedule exists", 400

        teacher_conflict = Schedule.query.filter_by(
            day=day,
            period=period,
            teacher_id=teacher_id
        ).first()

        if teacher_conflict:
            return "Teacher already assigned", 400

        s = Schedule(
            day=day,
            period=period,
            subject=subject,
            teacher_id=teacher_id,
            class_id=class_id,
            start_time=start_time,
            end_time=end_time
        )

        db.session.add(s)
        db.session.commit()
        return "Created"

    @app.route("/schedule/update", methods=["POST"])
    @role_required("admin")
    def update_schedule():
        id = int(request.form["id"])
        s = Schedule.query.get(id)

        if not s:
            return "Not found", 404

        s.day = request.form["day"]
        s.period = int(request.form["period"])
        s.subject = request.form["subject"]
        s.teacher_id = int(request.form["teacher_id"])

        db.session.commit()
        return "Updated"


    @app.route("/schedule/delete", methods=["POST"])
    @role_required("admin")
    def delete_schedule():
        id = int(request.form["id"])
        s = Schedule.query.get(id)

        if not s:
            return "Not found", 404

        db.session.delete(s)
        db.session.commit()
        return "Deleted"

    @app.route("/schedule/all")
    @role_required("admin")
    def all_schedule():
        data = Schedule.query.all()

        return {"schedule": [
            {
                "id": s.id,
                "day": s.day,
                "period": s.period,
                "subject": s.subject,
                "teacher_id": s.teacher_id,
                "class_id": s.class_id
            } for s in data
        ]}