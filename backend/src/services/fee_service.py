from datetime import timedelta, date
from src.db.model import db, Student, Fee, FeePlan


def generate_fees():

    today = date.today()

    students = Student.query.all()

    for s in students:

        # skip if left
        if s.leave_date and s.leave_date < today:
            continue

        plans = s.class_.fee_plans
        if not plans:
            continue

        plan = plans[0]  # or enforce 1 plan at DB level
        
        if not plan:
            continue

        # anchor (start of cycle)
        anchor = s.reactive_date or s.join_date
        if not anchor:
            continue

        # last fee
        last_fee = Fee.query.filter_by(student_id=s.id)\
            .order_by(Fee.period_end.desc()).first()

        if last_fee:
            start = last_fee.period_end + timedelta(days=1)
        else:
            start = anchor

        # generate only if due
        if start > today:
            continue

        # -------- calculate end date --------
        next_month = start.replace(day=28) + timedelta(days=4)
        try:
            end = next_month.replace(day=anchor.day) - timedelta(days=1)
        except:
            # handle months with fewer days
            end = next_month.replace(day=1) - timedelta(days=1)

        # prevent duplicate overlapping
        exists = Fee.query.filter_by(
            student_id=s.id,
            period_start=start,
            period_end=end
        ).first()

        if exists:
            continue

        fee = Fee(
            student_id=s.id,
            total=plan.monthly_amount,
            paid=0,
            status="due",
            period_start=start,
            period_end=end
        )

        db.session.add(fee)

    db.session.commit()