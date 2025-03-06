class Config:
    SECRET_KEY = "secret123"
    DAILY_LIMIT = 50  # Maximum patients per day
    TIME_SLOT_LIMIT = 5  # Maximum patients per time slot

# Hardcoded data storage
appointments = []
healthcare_workers = {}
appointment_slots = {}  # Format: {'YYYY-MM-DD': {'time': count}}
