# appointment.py 
from datetime import datetime

# Base Class (Appointment Data Representation)
class Appointment:
    def __init__(self, appointment_no: str, patient_name: str, vaccine_type: str, 
                 date: str, time: str, status: str, center: str):
        self.appointment_no = appointment_no
        self.patient_name = patient_name
        self.vaccine_type = vaccine_type
        self.date = date  # Keep as string for consistency with manage_appointments.py
        self.time = time  # Keep as string
        self.status = status
        self.center = center

    def to_dict(self):
        """Convert the object into a dictionary to match how manage_appointments.py accesses it."""
        return {
            "appointment_no": self.appointment_no,
            "patient_name": self.patient_name,
            "vaccine_type": self.vaccine_type,
            "date": self.date,  
            "time": self.time,  
            "status": self.status,
            "center": self.center
        }

    def __getitem__(self, key):
        """Allows dictionary-style access (appointment['status'])"""
        return getattr(self, key, None)
    
    def __setitem__(self, key, value):
        """Allows dictionary-style assignment (appointment['status'] = 'Cancelled')"""
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            raise KeyError(f"'{key}' is not a valid attribute of Appointment.")