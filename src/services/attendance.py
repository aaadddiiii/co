from datetime import date
from src.db.model import db, Schedule, TeacherAttendance


def mark_absent_teachers():
    today = date.today()

    schedules = Schedule.query.all()

    for s in schedules:
        exists = TeacherAttendance.query.filter_by(
            teacher_id=s.teacher_id,
            date=today,
            period=s.period
        ).first()

        if not exists:
            db.session.add(TeacherAttendance(
                teacher_id=s.teacher_id,
                date=today,
                period=s.period,
                status="absent"
            ))

    db.session.commit()