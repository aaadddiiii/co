from . import admin_attendance_routes, teacher_attendance_routes, student_attendance_routes, parent_attendance_routes

def routes(app):
    admin_attendance_routes.routes(app)
    teacher_attendance_routes.routes(app)
    student_attendance_routes.routes(app)
    parent_attendance_routes.routes(app)