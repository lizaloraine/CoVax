# Base Class (General Entity)
class Patient:
    """ Note: This implementation does not use a database. Instead, it relies on an in-memory list (`appointment_list`)
    to store appointments. This is for demonstration purposes and not meant for a fully functional system.
    """ 

    def __init__(self, patient_name, email, phone_number):
        self.patient_name = patient_name
        self.email = email
        self.phone_number = phone_number  

    def bookAppointment(self, appointment_list, appointment):
        """Book an appointment by adding it to the in-memory list (simulating database storage)."""
        appointment_list.append(appointment)

    def requestCancellation(self, appointment_list, appointment_no, verification_code):
        """Cancel an appointment if valid.
        
        - This method checks if the appointment exists in `appointment_list` and is not already cancelled.
        - A hardcoded verification code (`1234`) is used for simplicity.
        """
        for appointment in appointment_list:
            if appointment.appointment_no == appointment_no and appointment.status != "Cancelled":
                if verification_code == "1234":  # Simulated verification
                    appointment.status = "Cancelled"
                    return True  
        return False  
