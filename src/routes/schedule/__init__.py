from . import admin, teacher, student

def route(app):
    admin.route(app)
    teacher.route(app)
    student.route(app)