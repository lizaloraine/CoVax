from flask import Blueprint, request, jsonify, render_template
from datetime import datetime, timedelta  
from models.system import System
from config import appointments

manage_requests_bp = Blueprint("manage_requests", __name__)

@manage_requests_bp.route("/manage-requests", methods=["GET", "POST"])
def manage_requests():
    if request.method == "POST":
        data = request.get_json()
        ref_no = data.get("refNo")
        verification_code = data.get("verificationCode")
        action = data.get("action") 

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
