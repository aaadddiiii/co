import sys, os
from datetime import date, datetime, time
from werkzeug.security import generate_password_hash

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import app, db
from src.db.model import (
    User, Teacher, Student, Class,
    Schedule,
    StudentAttendance, TeacherAttendance,
    Fee, Payment
)

def run():
    with app.app_context():

        db.drop_all()
        db.create_all()

        # -------- USERS --------
        admin = User(name="Admin", email="admin@test.com", password=generate_password_hash("123"), role="admin")
        treasurer = User(name="Treasurer", email="treasurer@test.com", password=generate_password_hash("123"),role="treasurer")

        t1 = User(name="Teacher1", email="t1@test.com", password=generate_password_hash("123"), role="teacher")
        t2 = User(name="Teacher2", email="t2@test.com", password=generate_password_hash("123"), role="teacher")

        p1 = User(name="Parent1", email="p1@test.com", password=generate_password_hash("123"), role="parent")
        p2 = User(name="Parent2", email="p2@test.com", password=generate_password_hash("123"), role="parent")

        s1 = User(name="Student1", email="s1@test.com", password=generate_password_hash("123"), role="student")
        s2 = User(name="Student2", email="s2@test.com", password=generate_password_hash("123"), role="student")
        s3 = User(name="Student3", email="s3@test.com", password=generate_password_hash("123"), role="student")

        db.session.add_all([admin, t1, t2, p1, p2, s1, s2, s3, treasurer])
        db.session.flush()

        # -------- CLASS --------
        c1 = Class(name="Class A")
        c2 = Class(name="Class B")

        db.session.add_all([c1, c2])
        db.session.flush()

        # -------- TEACHERS --------
        teacher1 = Teacher(user_id=t1.id, type="permanent", pay_rate=500)
        teacher2 = Teacher(user_id=t2.id, type="temporary", pay_rate=200)

        # -------- STUDENTS --------
        student1 = Student(user_id=s1.id, class_id=c1.id, parent_id=p1.id, status="active", join_date=date(2026,4,1))
        student2 = Student(user_id=s2.id, class_id=c1.id, parent_id=p1.id, status="active", join_date=date(2026,4,1))
        student3 = Student(user_id=s3.id, class_id=c2.id, parent_id=p2.id, status="active", join_date=date(2026,4,1))

        db.session.add_all([teacher1, teacher2, student1, student2, student3])
        db.session.flush()

        # -------- SCHEDULE --------
        days = ["Monday","Tuesday","Wednesday","Thursday","Friday"]

        for i, day in enumerate(days):
            db.session.add(Schedule(
                day=day,
                period=1,
                subject="Math",
                teacher_id=teacher1.id,
                class_id=c1.id,
                start_time=time(10,0),
                end_time=time(11,0)
            ))

            db.session.add(Schedule(
                day=day,
                period=2,
                subject="Science",
                teacher_id=teacher2.id,
                class_id=c2.id,
                start_time=time(11,0),
                end_time=time(12,0)
            ))

        # -------- ATTENDANCE (history) --------
        for d in range(1,6):
            for s in [student1, student2]:
                db.session.add(StudentAttendance(
                    student_id=s.id,
                    class_id=c1.id,
                    date=date(2026,4,d),
                    period=1,
                    status="present" if d % 2 else "absent"
                ))

            db.session.add(TeacherAttendance(
                teacher_id=teacher1.id,
                date=date(2026,4,d),
                period=1,
                status="present"
            ))

        # -------- FEES --------
        fee1 = Fee(
            student_id=student1.id,
            total=1000,
            paid=500,
            period_start=date(2026,4,1),
            period_end=date(2026,4,30),
            status="pending"
        )

        fee2 = Fee(
            student_id=student2.id,
            total=1000,
            paid=1000,
            period_start=date(2026,4,1),
            period_end=date(2026,4,30),
            status="paid"
        )

        db.session.add_all([fee1, fee2])
        db.session.flush()

        # -------- PAYMENTS --------
        pmt1 = Payment(
            student_id=student1.id,
            amount=500,
            txn_id="TXN123",
            screenshot="test.png",
            status="pending",
            fee_id=fee1.id
        )

        pmt2 = Payment(
            student_id=student2.id,
            amount=1000,
            txn_id="TXN999",
            screenshot="test.png",
            status="verified",
            fee_id=fee2.id
        )

        db.session.add_all([pmt1, pmt2])

        db.session.commit()

        print("✅ FULL SEED COMPLETE")


if __name__ == "__main__":
    run()