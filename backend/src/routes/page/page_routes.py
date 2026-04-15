from flask import render_template, redirect, session

def routes(app):

    # ROOT
    @app.route("/")
    def root():
        user_id = session.get("user_id")
        role = session.get("role")

        if not user_id or not role:
            return render_template("auth/login.html")

        if role == "admin":
            return redirect("/admin/dashboard")
        elif role == "teacher":
            return redirect("/teacher/dashboard")
        elif role == "student":
            return redirect("/student/dashboard")
        elif role == "parent":
            return redirect("/parent/dashboard")
        elif role == "treasurer":
            return redirect("/treasurer/dashboard")

        return render_template("auth/login.html")

    # ================= PAGES =================

    @app.route("/admin/<path:path>")
    def admin_pages(path):
        return render_template(f"admin/{path}.html")



    @app.route("/teacher/<path:path>")
    def teacher_pages(path):
        return render_template(f"teacher/{path}.html")



    @app.route("/student/<path:path>")
    def student_pages(path):
        return render_template(f"student/{path}.html")



    @app.route("/parent/<path:path>")
    def parent_pages(path):
        return render_template(f"parent/{path}.html")



    @app.route("/treasurer/payment/<int:id>")
    def treasurer_payment(id):
        return render_template("treasurer/payment.html")

    @app.route("/treasurer/<path:path>")
    def treasurer_pages(path):
        return render_template(f"treasurer/{path}.html")