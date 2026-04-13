from flask import session


def route(app):
    @app.route("/logout")
    def logout():
        session.clear()
        return "Logged out"
