from flask import send_from_directory, current_app


def routes(app):

    @app.route("/uploads/<filename>")
    def uploaded_file(filename):
        return send_from_directory(
            current_app.config["UPLOAD_FOLDER"],
            filename
        )