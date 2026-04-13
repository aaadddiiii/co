import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = "dev-secret-key"  # change later

    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "database.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # optional (useful later)
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"

    UPLOAD_FOLDER = "static/uploads"