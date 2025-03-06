# Utility Class (Simulates User Authentication & Session Management)
class Session:
    """Handles user authentication and session management.
    
    ⚠ Note: In the UML diagram, this represents an actual session-based authentication system.
    However, in this implementation, we are using *hardcoded dictionaries* instead 
    of a real authentication mechanism (e.g., Flask session, database).
    
    In a fully functional system, these methods would interact with a real *session storage* 
    or *authentication system* (e.g., Flask-Login, OAuth, or a database).
    """

    @staticmethod
    def login(email, password, healthcare_workers):
        """ ⚠ Note: In a real system, this would:
            - Hash the entered password
            - Compare it against the stored hashed password in the database
            - Establish a session (e.g., Flask session)
        """
        if email in healthcare_workers and healthcare_workers[email].password == password:
            return True
        return False

    @staticmethod
    def logout():
        """ ⚠ Note: In a real system, this would:
            - Clear the session (Flask session)
            - Redirect the user to a login page
        """
        return "User logged out successfully"

    @staticmethod
    def register(worker, healthcare_workers):
        """ ⚠ Note: In a real system, this would:
            - Store the hashed password securely in a database
            - Perform email verification
            - Assign proper user roles and permissions
        """
        if worker.email in healthcare_workers:
            return False  # Email already registered
        healthcare_workers[worker.email] = worker
        return True