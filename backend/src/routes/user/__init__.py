from . import user_routes

def routes(app):
    user_routes.routes(app)