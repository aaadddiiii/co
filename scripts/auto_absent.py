from flask import Flask
from config import Config
from src.db.model import db
from src.services.attendance import mark_absent_teachers

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    mark_absent_teachers()
    print("Auto absent done")