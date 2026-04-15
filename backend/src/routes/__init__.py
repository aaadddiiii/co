from . import attendance, schedule, auth, fees, salary, analytics, user, common, page, accounts

def routes(app):
    attendance.routes(app)
    schedule.routes(app)
    auth.routes(app)
    fees.routes(app)
    salary.routes(app)
    analytics.routes(app)
    user.routes(app)
    common.routes(app)
    page.routes(app)
    accounts.routes(app)