from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# -------- USERS --------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)


# -------- TEACHERS --------
class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    type = db.Column(db.String(20))
    pay_rate = db.Column(db.Float)

    user = db.relationship("User", backref="teacher", uselist=False)


# -------- STUDENTS --------
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    parent_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'))
    status = db.Column(db.String(20))
    join_date = db.Column(db.Date)
    reactive_date = db.Column(db.Date, nullable=True)
    leave_date = db.Column(db.Date, nullable=True)

    user = db.relationship("User", foreign_keys=[user_id], backref="student", uselist=False)
    parent = db.relationship("User", foreign_keys=[parent_id], backref="children")
    class_ = db.relationship("Class", backref="students")


# -------- SCHEDULE --------
class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(20))
    period = db.Column(db.Integer)
    subject = db.Column(db.String(100))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'))  # FIXED FK
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)

    teacher = db.relationship("Teacher", backref="schedules")
    class_ = db.relationship("Class", backref="schedules")


# -------- ATTENDANCE --------
class StudentAttendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))  # FIXED
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'))      # FIXED
    date = db.Column(db.Date)
    period = db.Column(db.Integer)
    status = db.Column(db.String(10))

    student = db.relationship("Student", backref="attendance")

    __table_args__ = (db.UniqueConstraint('student_id', 'date', 'period'),)


class TeacherAttendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))  # FIXED
    date = db.Column(db.Date)
    period = db.Column(db.Integer)
    status = db.Column(db.String(10))

    teacher = db.relationship("Teacher", backref="attendance")

    __table_args__ = (db.UniqueConstraint('teacher_id', 'date', 'period'),)


# -------- MATERIALS --------
class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    file_url = db.Column(db.String(300))
    uploaded_by = db.Column(db.Integer, db.ForeignKey('user.id'))  # FIXED

    user = db.relationship("User", backref="materials")


# -------- FEES --------
class Fee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))  # FIXED
    total = db.Column(db.Float)
    paid = db.Column(db.Float, default=0)
    period_start = db.Column(db.Date)
    period_end = db.Column(db.Date)
    status = db.Column(db.String(20))

    student = db.relationship("Student", backref="fees")


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))  # FIXED
    amount = db.Column(db.Float)
    txn_id = db.Column(db.String(100))
    screenshot = db.Column(db.String(300))
    status = db.Column(db.String(20))
    fee_id = db.Column(db.Integer, db.ForeignKey('fee.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    fee = db.relationship("Fee", backref="payments")
    student = db.relationship("Student", backref="payments")


# -------- TEACHER PAYMENTS --------
class TeacherPayment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    total_classes = db.Column(db.Integer, default=0)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default="pending")  # pending, paid

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('teacher_id', 'month', 'year'),)


# -------- ACCOUNTS --------
class AccountLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(10))  # "credit" | "debit"
    amount = db.Column(db.Float)
    description = db.Column(db.String(200))
    reference_id = db.Column(db.Integer)  # fee_id or salary_id
    date = db.Column(db.DateTime, default=datetime.utcnow)


# -------- CLASS --------
class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))


class FeePlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'))  # FIXED
    monthly_amount = db.Column(db.Float)

    class_ = db.relationship("Class", backref="fee_plans")


db.Index('idx_account_date', AccountLog.date)
db.Index('idx_fee_status', Fee.status)
db.Index('idx_teacher_payment', TeacherPayment.teacher_id)