from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
from models.appointment import Appointment
from models.system import System
from config import Config, appointments, appointment_slots

appointments_bp = Blueprint("appointments", __name__)

@appointments_bp.route("/get-available-slots/<date>")
def get_available_slots(date):
    daily_count = sum(appointment_slots.get(date, {}).values())
    
    all_slots = [
        '09:00 AM', '09:30 AM', '10:00 AM', '10:30 AM',
        '11:00 AM', '11:30 AM', '02:00 PM', '02:30 PM',
        '03:00 PM', '03:30 PM', '04:00 PM'
    ]
 
    available_slots = [
        {"time": slot, "remaining": Config.TIME_SLOT_LIMIT - appointment_slots.get(date, {}).get(slot, 0)}
        for slot in all_slots
        if System.check_availability(appointment_slots, date, slot, Config.DAILY_LIMIT, Config.TIME_SLOT_LIMIT)
    ]
 
    return jsonify({
        "available_slots": available_slots,
        "daily_remaining": Config.DAILY_LIMIT - daily_count
    })

@appointments_bp.route("/appointment/new", methods=["GET", "POST"])
def new_appointment():
    if request.method == "POST":
        data = request.get_json()
        date, time = data.get("date"), data.get("timeSlot")

        if not date or not time:
            return jsonify({"success": False, "message": "Missing date or time"})

        if not System.check_availability(appointment_slots, date, time, Config.DAILY_LIMIT, Config.TIME_SLOT_LIMIT):
            return jsonify({"success": False, "message": "Time slot is full or daily limit reached"})

        appointment_slots.setdefault(date, {}).setdefault(time, 0)
        appointment_slots[date][time] += 1

        appointment = Appointment(
            data.get("refNo"), data.get("fullName"), data.get("vaccineType"), date, time, "Pending", data.get("center")
        )
        appointments.append(appointment)

        return jsonify({"success": True, "appointment": appointment.to_dict()})

    return render_template("appointment_form.html")

