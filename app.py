from flask import Flask, session
from routes.appointments import appointments_bp
from routes.manage_requests import manage_requests_bp
from routes.manage_appointments import manage_appointments_bp
from routes.auth import auth_bp
from routes.main import main_bp
from config import Config
import os

app = Flask(__name__)
app.secret_key = os.urandom(24) 

app.config.from_object(Config)

app.register_blueprint(appointments_bp)
app.register_blueprint(manage_requests_bp)
app.register_blueprint(manage_appointments_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)

@app.before_request
def clear_session_on_restart():
    """Clears session only if it hasn't been cleared yet in this session."""
    if not session.get("initialized"):
        session.clear()
        session["initialized"] = True 

if __name__ == "__main__":
    app.run(debug=True)
