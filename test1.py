import requests
from datetime import datetime

BASE = "http://127.0.0.1:5000"
s = requests.Session()


def print_res(label, r):
    try:
        print(label, r.json())
    except:
        print(label, r.text)


# -------- AUTH --------
def login(email, password):
    r = s.post(f"{BASE}/login", data={
        "email": email,
        "password": password
    })
    print_res("LOGIN:", r)


def logout():
    r = s.get(f"{BASE}/logout")
    print("LOGOUT:", r.text)


# -------- CREATE USER --------
def create_user(name, email, role, parent_id=None):
    data = {
        "name": name,
        "email": email,
        "password": "123",
        "role": role,
        "type": "permanent",
        "pay_rate": 100
    }

    if parent_id:
        data["parent_id"] = parent_id

    r = s.post(f"{BASE}/register", data=data)
    print_res("CREATE USER:", r)


# -------- GET IDs (IMPORTANT) --------
def get_ids():
    # assuming predictable order after fresh DB
    # admin=1, teacher_user=2, parent=3, students=4,5
    return {
        "teacher_id": 1,   # Teacher table ID (NOT user id)
        "class_id": 1,
        "student_ids": [1, 2]
    }


# -------- CREATE SCHEDULE --------
def create_schedule(ids):
    day = datetime.now().strftime("%A")

    r = s.post(f"{BASE}/schedule/create", data={
        "day": day,
        "period": 1,
        "subject": "Math",
        "teacher_id": ids["teacher_id"],
        "class_id": ids["class_id"],
        "start_time": "00:00",
        "end_time": "23:59"
    })
    print_res("SCHEDULE:", r)


# -------- MARK ATTENDANCE --------
def mark_attendance(ids):
    r = s.post(
        f"{BASE}/attendance/teacher/mark",
        json={
            "class_id": ids["class_id"],
            "period": 1,
            "students": [
                {"id": ids["student_ids"][0], "status": "present"},
                {"id": ids["student_ids"][1], "status": "absent"}
            ]
        }
    )
    print_res("MARK:", r)


# -------- VIEWS --------
def view_teacher():
    print_res("TEACHER:", s.get(f"{BASE}/attendance/teacher/self"))


def view_student():
    print_res("STUDENT:", s.get(f"{BASE}/attendance/student"))


def view_parent():
    print_res("PARENT:", s.get(f"{BASE}/attendance/parent"))


# -------- ADMIN UPDATE --------
def admin_update():
    r = s.post(f"{BASE}/attendance/admin/update", data={
        "id": 1,
        "type": "student",
        "status": "present"
    })
    print_res("ADMIN UPDATE:", r)


# -------- FLOW --------
if __name__ == "__main__":

    # fresh DB REQUIRED
    # rm database.db && python app.py

    login("admin@mail.com", "123")

    create_user("Teacher", "teacher@mail.com", "teacher")
    create_user("Parent", "parent@mail.com", "parent")
    create_user("Student1", "s1@mail.com", "student", parent_id=3)
    create_user("Student2", "s2@mail.com", "student", parent_id=3)

    ids = get_ids()

    create_schedule(ids)
    logout()

    # teacher
    login("teacher@mail.com", "123")
    mark_attendance(ids)
    view_teacher()
    logout()

    # student
    login("s1@mail.com", "123")
    view_student()
    logout()

    # parent
    login("parent@mail.com", "123")
    view_parent()
    logout()

    # admin
    login("admin@mail.com", "123")
    admin_update()
    logout()