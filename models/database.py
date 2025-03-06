# Utility Class (Simulates Database Storage)
class Database:
    """Simulates database operations such as storing and updating appointments.
    
    ⚠ Note: In the UML diagram, this represents an actual database with real queries.
    However, in this implementation, we are using *hardcoded dictionaries* instead 
    of a real database for demonstration purposes.
    
    In a fully functional system, these methods would execute SQL queries 
    (e.g., INSERT, UPDATE statements) to interact with a database.
    """

    @staticmethod
    def addAppointment(appointment_list, appointment):
        """ ⚠ Note: In a real database, this would execute:
            INSERT INTO appointments (appointment_no, patient_name, vaccine_type, date, time, status, center) 
            VALUES (...)
        """
        appointment_list.append(appointment)

    @staticmethod
    def updateAppointmentRecord(appointment_no, status, appointment_list):
        """ ⚠ Note: In a real system, this would execute:
            UPDATE appointments SET status = ? WHERE appointment_no = ?
        """
        for appointment in appointment_list:
            if appointment.appointment_no == appointment_no:
                appointment.status = status
                return True
        return False

    @staticmethod
    def storeHealthcareWorker(worker, healthcare_workers):
        """ ⚠ Note: In a real system, this would execute:
            INSERT INTO healthcare_workers (email, fullname, facility, license, password, is_admin) 
            VALUES (...)
        """
        healthcare_workers[worker.email] = worker