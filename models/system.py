# system.py
from config import appointment_slots, appointments

# Utility Class (Handles System Processes)
class System:

    @staticmethod
    def get_available_slots(date):
        """Return available time slots for a given date."""
        all_slots = [
            '09:00 AM', '09:30 AM', '10:00 AM', '10:30 AM',
            '11:00 AM', '11:30 AM', '02:00 PM', '02:30 PM',
            '03:00 PM', '03:30 PM', '04:00 PM'
        ]

        daily_count = sum(appointment_slots.get(date, {}).values())

        available_slots = [
            {"time": slot, "remaining": 5 - appointment_slots.get(date, {}).get(slot, 0)}
            for slot in all_slots if daily_count < 50
        ]
        return available_slots


    
    @staticmethod
    def check_availability(appointment_slots, date, time, daily_limit, time_slot_limit):
        """Check if a slot is available before booking.

        ⚠ Note: This function is required only because we are using a dictionary 
        instead of a real database. In a database-backed system, this logic would
        be handled using SQL queries or ORM calls.
        In a fully working system with a database (as shown in the UML diagram),
        availability checks would be handled via database queries instead of a dictionary.

        It ensures that:
        - The total daily appointments do not exceed daily_limit
        - The selected time slot does not exceed time_slot_limit
        """
        daily_count = sum(appointment_slots.get(date, {}).values())
        slot_count = appointment_slots.get(date, {}).get(time, 0)

        return daily_count < daily_limit and slot_count < time_slot_limit

    @staticmethod
    def verify_appointment(appointment_no, verification_code):
        for appointment in appointments:
            if appointment.appointment_no == appointment_no and verification_code == "1234":  # Dummy verification
                return True
        return False

    @staticmethod
    def check_status(appointment_no):
        appointment = next((a for a in appointments if a.appointment_no == appointment_no), None)
        return appointment.status if appointment else "Not Found"

    @staticmethod
    def request_cancellation(appointment_no):
        appointment = next((a for a in appointments if a.appointment_no == appointment_no), None)

        if not appointment:
            return "Appointment not found"

        if appointment.status == "Cancelled":
            return "Appointment is already cancelled"

        appointment.status = "Cancelled"
        return "Appointment successfully cancelled"