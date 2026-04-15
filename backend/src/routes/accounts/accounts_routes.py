from flask import request
from sqlalchemy import func
from datetime import datetime
from src.db.model import AccountLog, db
from src.utils import role_required, error, success


def routes(app):

    # -------- ALL TRANSACTIONS --------
    @app.route("/accounts/all")
    @role_required("admin", "treasurer")
    def all_transactions():
        logs = AccountLog.query.order_by(AccountLog.date.desc()).all()

        return success(data={
            "data": [
                {
                    "id": l.id,
                    "type": l.type,
                    "amount": l.amount,
                    "description": l.description,
                    "date": str(l.date)
                } for l in logs
            ]
        })


    # -------- SUMMARY --------
    @app.route("/accounts/summary")
    @role_required("admin", "treasurer")
    def summary():
        credit = db.session.query(func.sum(AccountLog.amount))\
            .filter_by(type="credit").scalar() or 0

        debit = db.session.query(func.sum(AccountLog.amount))\
            .filter_by(type="debit").scalar() or 0

        return success(data={
            "total_income": credit,
            "total_expense": debit,
            "balance": credit - debit
        })


    # -------- MONTHLY REPORT --------
    @app.route("/accounts/monthly")
    @role_required("admin", "treasurer")
    def monthly():

        month = request.args.get("month")
        if not month or not month.isdigit():
            return error("Invalid month")
        
        year = request.args.get("year")
        if not year or not year.isdigit():
            return error("Invalid year")



        month = int(month)
        year = int(year)

        logs = AccountLog.query.filter(
            func.extract('month', AccountLog.date) == month,
            func.extract('year', AccountLog.date) == year
        ).all()

        credit = sum(l.amount for l in logs if l.type == "credit")
        debit = sum(l.amount for l in logs if l.type == "debit")

        return success(data={
            "month": month,
            "year": year,
            "income": credit,
            "expense": debit,
            "balance": credit - debit
        })


    # -------- MANUAL ENTRY --------
    @app.route("/accounts/add", methods=["POST"])
    @role_required("admin")
    def add_entry():

        data = request.form

        type_, err = get_str(data, "type")
        if err: return err

        amount, err = get_float(data, "amount")
        if err: return err

        description = data.get("description", "").strip()

        if type_ not in ["credit", "debit"]:
            return error("Invalid type")

        log = AccountLog(
            type=type_,
            amount=amount,
            description=description
        )

        db.session.add(log)
        db.session.commit()

        return success(message="Added")