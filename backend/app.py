from flask import Flask
from config import Config
from src.db.model import db, User
from src.routes import routes
from werkzeug.security import generate_password_hash
from src.core.error_handler import init_error_handlers
from flask_cors import CORS



app = Flask(__name__)
CORS(app, supports_credentials=True)

app.config.from_object(Config)

db.init_app(app)
init_error_handlers(app)

# -------- INIT DB + CREATE ADMIN --------
with app.app_context():
    db.create_all()

    # create admin only if not exists
    if not User.query.filter_by(role="admin").first():
        admin = User(
            name="Admin",
            email="admin",
            password=generate_password_hash("123"),
            role="admin"
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin created")


# -------- REGISTER ROUTES --------
routes(app)


if __name__ == "__main__":
    app.run(debug=True)