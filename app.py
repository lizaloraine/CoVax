from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from datetime import datetime, timedelta

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

@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username] == password:
            session["user"] = username
            return redirect(url_for("home"))
        else:
            return render_template("login.html", error="Invalid credentials. Try again.")

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users:
            return render_template("register.html", error="Username already exists.")
        else:
            users[username] = password
            return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/home")
def home():
    if "user" in session:
        return render_template("home.html", user=session["user"])
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
