
from . import attendance, schedule, auth, fees

def route(app):
    attendance.route(app)
    schedule.route(app)
    auth.route(app)
    fees.route(app)