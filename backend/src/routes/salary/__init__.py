from . import admin_salary_routes, treasurer_salary_routes


def routes(app):
    admin_salary_routes.routes(app)
    treasurer_salary_routes.routes(app)