from flask import session


def routes(app):
    @app.route("/logout")
    def logout():
        session.clear()
        return "Logged out"
