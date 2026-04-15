from . import accounts_routes

def routes(app):
    accounts_routes.routes(app)