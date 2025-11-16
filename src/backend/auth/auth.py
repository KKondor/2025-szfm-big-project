from flask import Blueprint, request, render_template, redirect, session
from services.auth_service import login as backend_login
from services.auth_service import register as backend_register
from repository.users import User

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login_route():
    error_message = None
    if request.method == "POST":
        identifier = request.form["identifier"]
        password = request.form["password"]

        try:
            user = backend_login(identifier, password)
            if isinstance(user, User):
                session["user_id"] = user.id
                session["user_role"] = user.role.value
                session["user_email"] = user.email
                print(f"Bejelentkezett felhasználó: {user.name} (ID: {user.id}, Role: {user.role})")
                return redirect("/")
            else:
                error_message = "LogIn failed. Please try again."
        except Exception as e:
            error_message = str(e)

    return render_template("login.html", error_message=error_message)

@auth_bp.route("/register", methods=["GET", "POST"])
def register_route():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        phone = request.form.get("phone", "")
        address = request.form.get("address", "")

        try:
            backend_register(name, email, password, phone, address)
            return redirect("/login")
        except Exception as e:
            return render_template("register.html", error_message=str(e))

    return render_template("register.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
