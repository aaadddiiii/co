from src.db.model import db, Teacher, TeacherPayment, TeacherAttendance
from sqlalchemy import extract




def calculate_salary(teacher_id, month, year):
    teacher = Teacher.query.get(teacher_id)
    if not teacher:
        return 0, 0

    total_classes = TeacherAttendance.query.filter(
        TeacherAttendance.teacher_id == teacher_id,
        TeacherAttendance.status == "present",
        extract('month', TeacherAttendance.date) == month,
        extract('year', TeacherAttendance.date) == year
    ).count()

    if teacher.type == "temporary":
        amount = total_classes * teacher.pay_rate
    else:
        # permanent (fixed salary)
        amount = teacher.pay_rate

    return total_classes, amount




def generate_salary_for_all(month, year):
    teachers = Teacher.query.all()

    for teacher in teachers:
        existing = TeacherPayment.query.filter_by(
            teacher_id=teacher.id,
            month=month,
            year=year
        ).first()

        if existing:
            total_classes, amount = calculate_salary(teacher.id, month, year)
            existing.total_classes = total_classes
            existing.amount = amount
            continue

        result = calculate_salary(teacher.id, month, year)

        if not result:
            total_classes, amount = 0, 0
        else:
            total_classes, amount = result

        payment = TeacherPayment(
            teacher_id=teacher.id,
            month=month,
            year=year,
            total_classes=total_classes,
            amount=amount
        )

        db.session.add(payment)

    db.session.commit()