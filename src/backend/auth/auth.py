from flask import Blueprint, request, render_template, redirect, session
from services.auth_service import login as backend_login
from repository.users import User

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login_route():
    if request.method == "POST":
        identifier = request.form["identifier"]
        password = request.form["password"]

        user = backend_login(identifier, password)

        if isinstance(user, User):
            session["user_id"] = user.id
            session["user_role"] = user.role.value  #
            print(f"Bejelentkezett felhasználó: {user.name} (ID: {user.id}, Role: {user.role})")
            return redirect("/")

        # Ha nem User objektum, akkor hibaüzenet (string)
        return render_template("login.html", error=user)

    # GET kérés esetén csak a login oldalt mutatja
    return render_template("login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register_route():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        phone = request.form.get("phone", "")
        address = request.form.get("address", "")
        message = backend_register(name, email, password, phone, address)
        if message == "Regisztráció sikeres.":
            return redirect("/login")
        return message
    return render_template("register.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
