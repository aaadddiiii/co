from flask import request
from sqlalchemy import func, extract
from src.db.model import db, Student, Teacher, Fee, TeacherPayment, AccountLog
from src.utils import role_required, success, error


def routes(app):

    # -------- OVERVIEW --------
    @app.route("/analytics/overview")
    @role_required("admin")
    def overview():
        total_fees = db.session.query(func.sum(Fee.total)).scalar() or 0
        total_salary = db.session.query(func.sum(TeacherPayment.amount)).scalar() or 0

        return success(data={
            "students": Student.query.count(),
            "teachers": Teacher.query.count(),
            "total_fees": total_fees,
            "total_salary": total_salary
        })


    # -------- MONTHLY TREND --------
    @app.route("/analytics/monthly-trend")
    @role_required("admin")
    def monthly_trend():

        data = db.session.query(
            extract('month', AccountLog.date).label("month"),
            AccountLog.type,
            func.sum(AccountLog.amount)
        ).group_by(
            extract('month', AccountLog.date),
            AccountLog.type
        ).all()

        result = {}

        for month, type_, amount in data:
            month = int(month)

            if month not in result:
                result[month] = {"income": 0, "expense": 0}

            if type_ == "credit":
                result[month]["income"] = amount
            else:
                result[month]["expense"] = amount

        return success(data={"data": result})


    # -------- DEFAULTERS --------
    @app.route("/analytics/defaulters")
    @role_required("admin")
    def defaulters():

        fees = Fee.query.filter(Fee.status != "paid").all()

        return success(data={
            "data": [
                {
                    "student_id": f.student_id,
                    "due": f.total - f.paid,
                    "period_start": str(f.period_start),
                    "period_end": str(f.period_end)
                } for f in fees
            ]
        })


    # -------- DATE RANGE REPORT --------
    @app.route("/analytics/date-range")
    @role_required("admin")
    def date_range():
        start = request.args.get("start")  # YYYY-MM-DD
        end = request.args.get("end")

        if not start or not end:
            return error("Missing dates")
        
        try:
            start = date.fromisoformat(start)
            end = date.fromisoformat(end)
        except:
            return error("Invalid date format")

        logs = AccountLog.query.filter(
            AccountLog.date >= start,
            AccountLog.date <= end
        ).all()

        income = sum(l.amount for l in logs if l.type == "credit")
        expense = sum(l.amount for l in logs if l.type == "debit")

        return success(data={
            "income": income,
            "expense": expense,
            "balance": income - expense
        })


    # -------- TOP EARNERS (teachers) --------
    @app.route("/analytics/top-teachers")
    @role_required("admin")
    def top_teachers():

        data = db.session.query(
            TeacherPayment.teacher_id,
            func.sum(TeacherPayment.amount).label("total")
        ).group_by(TeacherPayment.teacher_id)\
         .order_by(func.sum(TeacherPayment.amount).desc())\
         .limit(5).all()

        return success(data={
            "data": [
                {"teacher_id": t_id, "total_salary": total}
                for t_id, total in data
            ]
        })