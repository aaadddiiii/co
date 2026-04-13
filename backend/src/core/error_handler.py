from src.utils.response import error

def init_error_handlers(app):

    @app.errorhandler(400)
    def bad_request(e):
        return error("Bad request", 400)

    @app.errorhandler(401)
    def unauthorized(e):
        return error("Unauthorized", 401)

    @app.errorhandler(403)
    def forbidden(e):
        return error("Forbidden", 403)

    @app.errorhandler(404)
    def not_found(e):
        return error("Not found", 404)

    @app.errorhandler(500)
    def server_error(e):
        return error("Server error", 500)