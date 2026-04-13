from . import admin_fee_routes, student_fee_routes, parent_fee_routes, treasurer_fee_routes

def routes(app):
    admin_fee_routes.routes(app)
    treasurer_fee_routes.routes(app)
    student_fee_routes.routes(app)
    parent_fee_routes.routes(app)