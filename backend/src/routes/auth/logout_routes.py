from flask import session


def routes(app):
    @app.route("/logout")
    def logout():
        session.clear()
        return success(message="Logged out")
