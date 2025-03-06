from werkzeug.security import generate_password_hash, check_password_hash

# Subclass (Manages Appointments) -> Extends Appointment Logic
class HealthcareWorker:
    def __init__(self, fullname, facility, license, email, password, is_admin=False):
        self.fullname = fullname
        self.facility = facility
        self.license = license
        self.email = email
        self.password = generate_password_hash(password)  # For password hashing
        self.is_admin = is_admin

    def check_password(self, password):
        # Check if the provided password matches the stored hashed password.
        return check_password_hash(self.password, password)

    def approve_appointment(self, appointment_list, appointment_no):
        # Approve an appointment if status is pending.
        for appointment in appointment_list:
            if appointment.appointment_no == appointment_no and appointment.status == "Pending":
                appointment.status = "Confirmed"
                return True
        return False
