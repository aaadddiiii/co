from . import login_routes, register_routes, logout_routes

def routes(app):
    login_routes.routes(app)
    register_routes.routes(app)
    logout_routes.routes(app)
