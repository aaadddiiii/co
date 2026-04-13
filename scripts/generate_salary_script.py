import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app
from src.services.payroll_service import generate_salary_for_all
from datetime import datetime


with app.app_context():
    today = datetime.today()

    generate_salary_for_all(today.month, today.year)

    print("Salary generated")