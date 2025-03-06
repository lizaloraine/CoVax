from flask import Blueprint, render_template, session, redirect, url_for
from datetime import datetime 
from config import healthcare_workers, appointments 
from models.appointment import Appointment

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def landing():
    user_data = None
    fullname = None

    if "user" in session:
        user_email = session["user"]
        user_data = healthcare_workers.get(user_email, {})
        fullname = user_data.get("fullname", user_email)
    
    return render_template("landing.html", 
                         is_logged_in="user" in session,
                         user=fullname if "user" in session else None)
@main_bp.route("/home")
def home():
    if "user" in session:
        user_email = session["user"]
        user_data = healthcare_workers.get(user_email, {})
        fullname = user_data.get("fullname", user_email)  
        
        stats = {
            "total": len(appointments),
            "pending": sum(1 for a in appointments if isinstance(a, Appointment) and a.status == "Pending"),
            "confirmed": sum(1 for a in appointments if isinstance(a, Appointment) and a.status == "Confirmed"),
            "cancelled": sum(1 for a in appointments if isinstance(a, Appointment) and a.status == "Cancelled"),
        }

        return render_template("home.html", 
                             user=fullname, 
                             stats=stats,
                             current_date=datetime.now().strftime("%B %d, %Y"))
    return redirect(url_for("auth.login"))
