import requests
import subprocess
from datetime import datetime

BASE = "http://127.0.0.1:5000"


def safe(res):
    print("Status:", res.status_code)
    try:
        print(res.json())
    except:
        print(res.text)


def login(session, email, password):
    res = session.post(f"{BASE}/login", data={
        "email": email,
        "password": password
    })
    return res.status_code == 200


def create_user(admin, payload):
    res = admin.post(f"{BASE}/register", data=payload)
    return res.status_code in (200, 500)


def get_user_id(admin, email):
    res = admin.get(f"{BASE}/users")
    users = res.json()

    for u in users:
        if u["email"] == email:
            return u["id"]
    return None


def get_class_id(admin):
    res = admin.get(f"{BASE}/classes")

    try:
        classes = res.json()
    except:
        classes = []

    if not classes:
        admin.post(f"{BASE}/class/create", data={
            "name": "TestClass"
        })
        return 1

    return classes[0]["id"]


if __name__ == "__main__":

    # ---------- ADMIN ----------
    admin = requests.Session()
    if not login(admin, "admin@mail.com", "123"):
        print("Admin login failed")
        exit()

    # ---------- ENSURE USERS ----------
    create_user(admin, {
        "name": "Treasurer",
        "email": "treasurer@mail.com",
        "password": "123",
        "role": "treasurer"
    })

    create_user(admin, {
        "name": "Teacher1",
        "email": "teacher@mail.com",
        "password": "123",
        "role": "teacher",
        "type": "temporary",
        "pay_rate": "100"
    })

    # ---------- LOGIN USERS ----------
    treasurer = requests.Session()
    login(treasurer, "treasurer@mail.com", "123")

    teacher = requests.Session()
    login(teacher, "teacher@mail.com", "123")

    # ---------- GET IDS ----------
    teacher_id = get_user_id(admin, "teacher@mail.com")
    class_id = get_class_id(admin)

    if not teacher_id:
        print("Teacher not found")
        exit()

    # ---------- CREATE SCHEDULE ----------
    day = datetime.today().strftime("%A")

    admin.post(f"{BASE}/schedule/create", data={
        "day": day,
        "period": 1,
        "subject": "Math",
        "teacher_id": teacher_id,
        "class_id": class_id,
        "start_time": "00:00",
        "end_time": "23:59"
    })

    # ---------- MARK ATTENDANCE ----------
    print("\n[MARK ATTENDANCE]")

    # force create valid attendance directly (bypass schedule validation)
    res = teacher.post(f"{BASE}/attendance/teacher/mark", json={
        "class_id": class_id,
        "period": 1,
        "students": []
    })

    safe(res)

    # if still forbidden → force insert via admin (fallback)
    if res.status_code == 403:
        print("⚠️ Forcing attendance via admin fallback")

        admin.post(f"{BASE}/attendance/admin/mark", json={
            "teacher_id": teacher_id,
            "class_id": class_id,
            "period": 1,
            "date": datetime.today().strftime("%Y-%m-%d"),
            "status": "present"
        })

    # ---------- GENERATE SALARY ----------
    print("\n[GENERATE SALARY]")
    subprocess.run(["python", "-m", "scripts.generate_salary_script"])

    # ---------- VIEW SALARY ----------
    print("\n[VIEW SALARY]")
    res = treasurer.get(f"{BASE}/salary/all")
    safe(res)

    salaries = res.json().get("salaries", [])
    if not salaries:
        print("No salary generated")
        exit()

    payment_id = salaries[0]["id"]

    # ---------- PAY ----------
    print("\n[PAY SALARY]")
    res = treasurer.post(f"{BASE}/salary/pay", data={
        "payment_id": payment_id
    })
    safe(res)

    # ---------- DOUBLE PAY ----------
    print("\n[DOUBLE PAY CHECK]")
    res = treasurer.post(f"{BASE}/salary/pay", data={
        "payment_id": payment_id
    })
    safe(res)

    # ---------- ADMIN VIEW ----------
    print("\n[ADMIN VIEW]")
    res = admin.get(f"{BASE}/salary/admin")
    safe(res)