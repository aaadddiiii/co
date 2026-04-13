from . import admin, student, parent, treasurer

def route(app):
    admin.route(app)
    treasurer.route(app)
    student.route(app)
    parent.route(app)