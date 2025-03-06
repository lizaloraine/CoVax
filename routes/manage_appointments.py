from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
from config import appointments
from models.appointment import Appointment 

manage_appointments_bp = Blueprint("manage_appointments", __name__)

@manage_appointments_bp.route("/approve-appointment", methods=["POST"])
def approve_appointment():
    if "user" not in session:
        return jsonify({"success": False, "message": "Unauthorized"}), 401
    
    data = request.get_json()
    appointment_no = data.get("appointment_no")
    
    appointment = next((a for a in appointments if a.appointment_no == appointment_no), None)
    
    if not appointment:
        return jsonify({"success": False, "message": "Appointment not found"})
    
    if appointment.status != "Pending":
        return jsonify({"success": False, "message": "Can only approve pending appointments"})
    
    appointment.status = "Confirmed"
    return jsonify({"success": True})

@manage_appointments_bp.route("/cancel-appointment", methods=["POST"])
def cancel_appointment():
    if "user" not in session:
        return jsonify({"success": False, "message": "Unauthorized"}), 401
    
    data = request.get_json()
    appointment_no = data.get("appointment_no")
    
    appointment = next((a for a in appointments if a.appointment_no == appointment_no), None)
    
    if not appointment:
        return jsonify({"success": False, "message": "Appointment not found"})
    
    if appointment.status == "Cancelled":
        return jsonify({"success": False, "message": "Appointment is already cancelled"})
    
    appointment.status = "Cancelled"
    return jsonify({"success": True})

@manage_appointments_bp.route("/get-appointment/<appointment_no>")
def get_appointment(appointment_no):
    if "user" not in session:
        return jsonify({"success": False, "message": "Unauthorized"}), 401
   
    appointment = next((a for a in appointments if a.appointment_no == appointment_no), None)
    
    if not appointment:
        return jsonify({"success": False, "message": "Appointment not found"})
    
    return jsonify({
        "success": True,
        "appointment": appointment.to_dict() 
    })

@manage_appointments_bp.route("/appointment")
def appointment():
    if "user" in session:
        return render_template("appointment.html", user=session["user"], appointments=[a.to_dict() for a in appointments])
    return redirect(url_for("auth.login"))
