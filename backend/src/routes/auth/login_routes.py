from src.utils.validators import require_fields
from src.utils.response import success, error

@app.route("/login", methods=["POST"])
def login():
    data = request.form

    err = require_fields(data, ["email", "password"])
    if err:
        return error(err)

    user = User.query.filter_by(email=data["email"]).first()

    if not user or not check_password_hash(user.password, data["password"]):
        return error("Invalid credentials", 401)

    session["user_id"] = user.id
    session["role"] = user.role

    return success(message="Logged in")