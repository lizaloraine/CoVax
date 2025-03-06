from flask import Blueprint, request, session, redirect, url_for, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from models.healthcare_worker import HealthcareWorker
import re
from config import healthcare_workers

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        if email in healthcare_workers:
            worker = healthcare_workers[email]  
            stored_hash = worker["password"]


            if check_password_hash(stored_hash, password):  
                session["user"] = email
                return redirect(url_for("main.home"))

        print("Invalid email or password!")
        return render_template("login.html", error="Invalid email or password")

    return render_template("login.html")




@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        fullname = request.form["fullname"]
        facility = request.form["facility"]
        license = request.form["license"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm-password"]

        # Basic validation
        if not re.match(r"^\d{4}-\d{4}$", license):
            return render_template("register.html", 
                error="Invalid license number format")

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return render_template("register.html", 
                error="Invalid email address format")

        if password != confirm_password:
            return render_template("register.html", 
                error="Passwords do not match")

        if email in healthcare_workers:
            return render_template("register.html", 
                error="Email already registered")

        # Create new healthcare worker account
        healthcare_workers[email] = {
            "fullname": fullname,
            "facility": facility,
            "license": license,
            "password": generate_password_hash(password),
            "is_admin": True
        }

        session["user"] = email
        return redirect(url_for("main.home"))

    return render_template("register.html")

@auth_bp.route("/forgot-password")
def forgot_password():
    # Implement password recovery logic
    return "Password recovery functionality coming soon"


@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("main.landing"))