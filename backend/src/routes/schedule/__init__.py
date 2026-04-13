from . import admin_schedule_routes, teacher_schedule_routes, student_schedule_routes

def routes(app):
    admin_schedule_routes.routes(app)
    teacher_schedule_routes.routes(app)
    student_schedule_routes.routes(app)