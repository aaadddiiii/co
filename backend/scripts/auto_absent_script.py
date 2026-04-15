import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from flask import Flask
from config import Config
from src.db.model import db
from src.services.attendance import mark_absent_teachers
from app import app

db.init_app(app)

with app.app_context():
    mark_absent_teachers()
    print("Auto absent done")