from app import app
from src.db.model import db, User, Class
from werkzeug.security import generate_password_hash

def run_tests():
    client = app.test_client()
    client.testing = True

    print("---- TEST START ----")

    with client:

        # -------- LOGIN ADMIN --------
        res = client.post("/login", data={
            "email": "admin@mail.com",
            "password": "123"
        })
        print("Admin login:", res.data)

        # -------- CREATE CLASS --------
        with app.app_context():
            c = Class(name="Batch A")
            db.session.add(c)
            db.session.commit()

        # -------- CREATE USERS --------
        def create_user(data):
            return client.post("/register", data=data)

        create_user({
            "name": "Teacher1",
            "email": "t@mail.com",
            "password": "123",
            "role": "teacher",
            "type": "permanent",
            "pay_rate": "100"
        })

        create_user({
            "name": "Parent1",
            "email": "p@mail.com",
            "password": "123",
            "role": "parent"
        })

        create_user({
            "name": "Student1",
            "email": "s@mail.com",
            "password": "123",
            "role": "student",
            "parent_id": "2",
            "class_id": "1"
        })

        print("Users created")

        # -------- CREATE SCHEDULE --------
        res = client.post("/schedule/create", data={
            "day": "Monday",
            "period": "1",
            "subject": "Math",
            "teacher_id": "1",
            "class_id": "1",
            "start_time": "10:00",
            "end_time": "11:00"
        })
        print("Schedule:", res.data)

        # -------- DUPLICATE SCHEDULE TEST --------
        res = client.post("/schedule/create", data={
            "day": "Monday",
            "period": "1",
            "subject": "Science",
            "teacher_id": "1",
            "class_id": "1",
            "start_time": "10:00",
            "end_time": "11:00"
        })
        print("Duplicate schedule (should fail):", res.data)

        # -------- CREATE FEE --------
        res = client.post("/fees/create", data={
            "student_id": "1",
            "total": "500"
        })
        print("Fee:", res.data)

        # -------- STUDENT LOGIN --------
        client.get("/logout")
        client.post("/login", data={
            "email": "s@mail.com",
            "password": "123"
        })

        # -------- PAY --------
        res = client.post("/fees/pay", data={
            "fee_id": "1",
            "amount": "200",
            "txn_id": "TXN123"
        })
        print("Payment:", res.data)

        # -------- TREASURER SETUP --------
        client.get("/logout")

        with app.app_context():
            t = User(
                name="Treasurer",
                email="tre@mail.com",
                password=generate_password_hash("123"),
                role="treasurer"
            )
            db.session.add(t)
            db.session.commit()

        client.post("/login", data={
            "email": "tre@mail.com",
            "password": "123"
        })

        # -------- VERIFY PAYMENT --------
        res = client.post("/fees/verify", data={
            "payment_id": "1"
        })
        print("Verify:", res.data)
        client.get("/logout")


        # -------- CHECK FEES --------
        client.post("/login", data={
            "email": "admin@mail.com",
            "password": "123"
        })
        res = client.get("/fees/all")
        print("Fees after payment:", res.json)

    print("---- TEST END ----")


if __name__ == "__main__":
    with app.app_context():
        run_tests()