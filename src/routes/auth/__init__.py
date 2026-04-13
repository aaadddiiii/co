from . import login, register, logout

def route(app):
    login.route(app)
    register.route(app)
    logout.route(app)
