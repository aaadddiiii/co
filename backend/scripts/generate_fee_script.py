from flask import Flask
from config import Config
from src.db.model import db
from src.services.fees import generate_fees
from app import app


with app.app_context():
    generate_fees()
    print("Fees generated")