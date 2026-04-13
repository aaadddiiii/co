from datetime import date
from src.db.model import db, Schedule, TeacherAttendance


def mark_absent_teachers():
    today = date.today()

    now = datetime.now()
    today = now.date()
    current_day = now.strftime("%A")
    current_time = now.time()

    schedules = Schedule.query.filter_by(day=current_day).all()

    for s in schedules:
        if not (s.start_time <= current_time <= s.end_time):
            continue

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