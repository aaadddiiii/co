from . import attendance, schedule, auth, fees, salary

def routes(app):
    attendance.routes(app)
    schedule.routes(app)
    auth.routes(app)
    fees.routes(app)
    salary.routes(app)