from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import re

app = Flask(__name__)
app.secret_key = "secret123"  # Used for session handling

# Hardcoded users (username: password)
users = {
    "admin": "password123",
    "lizaloraine": "lizaloraine"
}

# Store appointments in memory (replace with database in production)
appointments = []

# Add slot limits configuration
DAILY_LIMIT = 50  # Maximum patients per day
TIME_SLOT_LIMIT = 5  # Maximum patients per time slot

# Track appointment slots
appointment_slots = {}  # Format: {'YYYY-MM-DD': {'time': count}}

# Add healthcare worker model
healthcare_workers = {}  # In production, use a database

@app.route("/get-available-slots/<date>")
def get_available_slots(date):
    daily_count = 0
    slots_status = {}
    
    # Get all time slots for the date
    if date in appointment_slots:
        daily_count = sum(appointment_slots[date].values())
        slots_status = appointment_slots[date]
    
    # Default time slots
    all_slots = [
        '09:00 AM', '09:30 AM', '10:00 AM', '10:30 AM',
        '11:00 AM', '11:30 AM', '02:00 PM', '02:30 PM',
        '03:00 PM', '03:30 PM', '04:00 PM'
    ]
    
    # Check availability
    available_slots = []
    for slot in all_slots:
        slot_count = slots_status.get(slot, 0)
        if slot_count < TIME_SLOT_LIMIT and daily_count < DAILY_LIMIT:
            available_slots.append({
                'time': slot,
                'remaining': TIME_SLOT_LIMIT - slot_count
            })
    
    return jsonify({
        'available_slots': available_slots,
        'daily_remaining': DAILY_LIMIT - daily_count
    })

@app.route("/appointment/new", methods=["GET", "POST"])
def new_appointment():
    if request.method == "POST":
        appointment_data = request.get_json()
        date = appointment_data["date"]
        time = appointment_data["timeSlot"]
        
        # Initialize date in appointment_slots if not exists
        if date not in appointment_slots:
            appointment_slots[date] = {}
        
        # Initialize time slot if not exists
        if time not in appointment_slots[date]:
            appointment_slots[date][time] = 0
            
        # Check if slot is still available
        daily_count = sum(appointment_slots[date].values())
        slot_count = appointment_slots[date][time]
        
        if daily_count >= DAILY_LIMIT:
            return jsonify({
                "success": False,
                "message": "No more appointments available for this date"
            })
            
        if slot_count >= TIME_SLOT_LIMIT:
            return jsonify({
                "success": False,
                "message": "This time slot is full"
            })
        
        # Increment slot counter
        appointment_slots[date][time] += 1
        
        # Create appointment
        appointment = {
            "appointment_no": appointment_data["refNo"],
            "patient_name": appointment_data["fullName"],
            "vaccine_type": appointment_data["vaccineType"],
            "date": date,
            "time": time,
            "status": "Pending",
            "center": appointment_data["center"]
        }
        appointments.append(appointment)
        return jsonify({"success": True, "appointment": appointment})
        
    return render_template("appointment_form.html")

@app.route("/manage-requests", methods=["GET", "POST"])
def manage_requests():
    if request.method == "POST":
        data = request.get_json()
        ref_no = data.get("refNo")
        verification_code = data.get("verificationCode")
        action = data.get("action") 

        # Find the appointment
        appointment = next((appt for appt in appointments if appt["appointment_no"] == ref_no), None)

        if not appointment:
            return jsonify({"success": False, "message": "Appointment not found"})

        try:
            appointment_datetime = datetime.strptime(f"{appointment['date']} {appointment['time']}", "%Y-%m-%d %I:%M %p")
        except ValueError as e:
            return jsonify({"success": False, "message": f"Error parsing appointment datetime: {str(e)}"})

        current_datetime = datetime.now()

        # Simulate user verification (dummy data)
        if action == "cancel_request" and verification_code != "1234":
            return jsonify({"success": False, "message": "Invalid verification code"})

        def censor_name(name):
            parts = name.split()
            censored = []
            for part in parts:
                if len(part) > 1:
                    censored.append(part[0] + '*' * (len(part) - 1))
                else:
                    censored.append(part)
            return ' '.join(censored)

        censored_name = censor_name(appointment["patient_name"])

        if action == "check_status":
            # Return appointment details
            return jsonify({
                "success": True,
                "appointment": {
                    "date": appointment["date"],
                    "time": appointment["time"],
                    "patient_name": censored_name, 
                    "center": appointment["center"],
                    "status": appointment["status"]
                }
            })
        elif action == "cancel_request":
            # Check if the cancellation is within 24 hours
            if appointment_datetime - current_datetime <= timedelta(hours=24):
                return jsonify({"success": False, "message": "Cannot cancel the appointment within 24 hours of the scheduled time"})
            
            # Simulate user verification (dummy data)
            if verification_code != "1234":
                return jsonify({"success": False, "message": "Invalid verification code"})
            
            appointment["status"] = "Cancelled"
            censored_name = censor_name(appointment["patient_name"])
            return jsonify({
                "success": True,
                "appointment": {
                    "date": appointment["date"],
                    "time": appointment["time"],
                    "patient_name": censored_name, 
                    "center": appointment["center"]
                },
                "message": "Appointment cancelled successfully"
            })

        else:
            return jsonify({"success": False, "message": "Invalid action"})

    return render_template("requests_form.html")

@app.route("/approve-appointment", methods=["POST"])
def approve_appointment():
    if "user" not in session:
        return jsonify({"success": False, "message": "Unauthorized"}), 401
    
    data = request.get_json()
    appointment_no = data.get("appointment_no")
    
    # Find the appointment
    appointment = next((a for a in appointments if a["appointment_no"] == appointment_no), None)
    
    if not appointment:
        return jsonify({"success": False, "message": "Appointment not found"})
    
    if appointment["status"] != "Pending":
        return jsonify({"success": False, "message": "Can only approve pending appointments"})
    
    # Update appointment status
    appointment["status"] = "Confirmed"
    return jsonify({"success": True})

@app.route("/cancel-appointment", methods=["POST"])
def cancel_appointment():
    if "user" not in session:
        return jsonify({"success": False, "message": "Unauthorized"}), 401
    
    data = request.get_json()
    appointment_no = data.get("appointment_no")
    
    # Find the appointment
    appointment = next((a for a in appointments if a["appointment_no"] == appointment_no), None)
    
    if not appointment:
        return jsonify({"success": False, "message": "Appointment not found"})
    
    if appointment["status"] == "Cancelled":
        return jsonify({"success": False, "message": "Appointment is already cancelled"})
    
    # Update appointment status
    appointment["status"] = "Cancelled"
    return jsonify({"success": True})

@app.route("/get-appointment/<appointment_no>")
def get_appointment(appointment_no):
    if "user" not in session:
        return jsonify({"success": False, "message": "Unauthorized"}), 401
    
    # Find the appointment
    appointment = next((a for a in appointments if a["appointment_no"] == appointment_no), None)
    
    if not appointment:
        return jsonify({"success": False, "message": "Appointment not found"})
    
    # Format the appointment data
    formatted_appointment = {
        "appointment_no": appointment["appointment_no"],
        "patient_name": appointment["patient_name"],
        "phone": appointment.get("phone", "N/A"),  # Use get() to handle missing fields
        "center": appointment["center"],
        "date": appointment["date"],
        "time": appointment["time"],
        "vaccine_type": appointment["vaccine_type"],
        "status": appointment["status"]
    }
    
    return jsonify({
        "success": True,
        "appointment": formatted_appointment
    })

@app.route("/")
def landing():
    # Get user data if logged in
    user_data = None
    if "user" in session:
        user_email = session["user"]
        user_data = healthcare_workers.get(user_email, {})
        fullname = user_data.get("fullname", user_email)
    
    return render_template("landing.html", 
                         is_logged_in="user" in session,
                         user=fullname if "user" in session else None)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        if email in healthcare_workers and \
           check_password_hash(healthcare_workers[email]["password"], password):
            session["user"] = email
            return redirect(url_for("home"))
        else:
            return render_template("login.html", 
                error="Invalid email or password")

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
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
                error="Invalid email address")

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
        return redirect(url_for("home"))

    return render_template("register.html")

@app.route("/forgot-password")
def forgot_password():
    # Implement password recovery logic
    return "Password recovery functionality coming soon"

@app.route("/home")
def home():
    if "user" in session:
        # Get the healthcare worker's full name
        user_email = session["user"]
        user_data = healthcare_workers.get(user_email, {})
        fullname = user_data.get("fullname", user_email)  # fallback to email if fullname not found
        
        stats = {
            'total': len(appointments),
            'pending': sum(1 for a in appointments if a['status'] == 'Pending'),
            'confirmed': sum(1 for a in appointments if a['status'] == 'Confirmed'),
            'cancelled': sum(1 for a in appointments if a['status'] == 'Cancelled')
        }
        return render_template("home.html", 
                             user=fullname,  # Pass fullname instead of email
                             stats=stats,
                             current_date=datetime.now().strftime("%B %d, %Y"))
    return redirect(url_for("login"))

@app.route("/appointment")
def appointment():
    if "user" in session:
        return render_template("appointment.html", user=session["user"], appointments=appointments)
    return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("landing"))

if __name__ == "__main__":
    app.run(debug=True)
