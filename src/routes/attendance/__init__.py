from . import admin, teacher, student, parent

def route(app):
    admin.route(app)
    teacher.route(app)
    student.route(app)
    parent.route(app)