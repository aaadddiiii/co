from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# -------- USERS --------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin, teacher, student, parent, treasurer


# -------- TEACHERS --------
class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    type = db.Column(db.String(20))  # permanent / temporary
    pay_rate = db.Column(db.Float)  # per period (temp) or monthly (permanent)


# -------- STUDENTS --------
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    parent_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'))
    status = db.Column(db.String(20))  
    # active / inactive / left
    join_date = db.Column(db.Date)
    reactive_date = db.Column(db.Date, nullable=True)
    leave_date = db.Column(db.Date, nullable=True)


# -------- SCHEDULE --------
class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(20))
    period = db.Column(db.Integer)
    subject = db.Column(db.String(100))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    class_id = db.Column(db.Integer)  # batch/class
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)


# -------- ATTENDANCE --------
class StudentAttendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer)
    class_id = db.Column(db.Integer)
    date = db.Column(db.Date)
    period = db.Column(db.Integer)
    status = db.Column(db.String(10))
    __table_args__ = (db.UniqueConstraint('student_id', 'date', 'period'),)


class TeacherAttendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer)
    date = db.Column(db.Date)
    period = db.Column(db.Integer)
    status = db.Column(db.String(10))  # present / absent
    __table_args__ = (db.UniqueConstraint('teacher_id', 'date', 'period'),)


# -------- MATERIALS --------
class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    file_url = db.Column(db.String(300))
    uploaded_by = db.Column(db.Integer)


# -------- FEES --------
class Fee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer)
    total = db.Column(db.Float)
    paid = db.Column(db.Float, default=0)
    period_start = db.Column(db.Date)
    period_end = db.Column(db.Date)
    status = db.Column(db.String(20))  # due / paid


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer)
    amount = db.Column(db.Float)
    txn_id = db.Column(db.String(100))
    screenshot = db.Column(db.String(300))
    status = db.Column(db.String(20))  # pending / verified
    fee_id = db.Column(db.Integer, db.ForeignKey('fee.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# -------- TEACHER PAYMENTS --------
class TeacherPayment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer)
    month = db.Column(db.String(20))
    total_amount = db.Column(db.Float)
    status = db.Column(db.String(20))  # pending / paid


# -------- ACCOUNTS --------
class AccountLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(10))  # income / expense
    amount = db.Column(db.Float)
    description = db.Column(db.String(200))
    date = db.Column(db.DateTime, default=datetime.utcnow)

# -------- Class --------
class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))


class FeePlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer)
    monthly_amount = db.Column(db.Float)