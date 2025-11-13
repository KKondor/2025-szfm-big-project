from flask import Blueprint, request, render_template, redirect, session
from backend.services.auth_service import login as backend_login
from backend.repository.users import User

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login_route():
    if request.method == "POST":
        identifier = request.form["identifier"]
        password = request.form["password"]

        user = backend_login(identifier, password)

        if isinstance(user, User):
            session["user_id"] = user.id
            session["user_role"] = user.role.value  # vagy user.role, ha nem Enum
            print(f"Bejelentkezett felhasználó: {user.name} (ID: {user.id}, Role: {user.role})")
            return redirect("/dashboard")

        # Ha nem User objektum, akkor hibaüzenet (string)
        return render_template("login.html", error=user)

    # GET kérés esetén csak a login oldalt mutatja
    return render_template("login.html")
