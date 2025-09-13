# model/operations.py
from pony.orm import db_session, select, delete, commit, count
from werkzeug.security import generate_password_hash
from datetime import date, datetime, timedelta

from model.user import User, Patient, Doctor, GlucoseReading, Symptom, Therapy, MedicationIntake, Alert

# Database initialization
@db_session
def initialize_db():

    # here we create our dummy data
    if User.select().count() == 0:
        # Create a doctor
        doctor_user = User(username='dr_smith', password_hash=generate_password_hash('doctorpass'), role='doctor')
        doctor = Doctor(user=doctor_user)
        
        # Create a patient
        patient_user = User(username='patient1', password_hash=generate_password_hash('patientpass'), role='patient')
        patient = Patient(user=patient_user, assigned_doctor=doctor)
        
        # Create sample data
        # Sample glucose reading
        GlucoseReading(
            patient=patient,
            value=120.5,
            measurement_time=datetime.now(),
            is_before_meal=True
        )
        
        # Sample therapy
        Therapy(
            patient=patient,
            doctor=doctor,
            drug_name="Metformin",
            daily_doses=2,
            dose_amount=500,
            dose_unit="mg",
            instructions="Take with meals",
            start_date=datetime.now()
        )

# User management functions
@db_session
def get_user(user_id):
    """Get a user by ID"""
    try:
        return User[int(user_id)]
    except (ValueError, TypeError):
        return None
    except Exception:  # This catches ObjectNotFound and any other Pony ORM exceptions
        return None

@db_session
def get_user_by_username(username):
    """Get a user by username"""
    return User.get(username=username)

@db_session
def add_user(username, password, role='patient'):
    """Add a new user to the database"""
    if User.get(username=username):
        return False

    user = User(
        username=username,
        password_hash=generate_password_hash(password),
        role=role
    )
    
    # Create corresponding Patient or Doctor record
    if role == 'patient':
        Patient(user=user)
    elif role == 'doctor':
        Doctor(user=user)
    
    return True

@db_session
def validate_user(username, password):
    """Validate user credentials"""
    user = User.get(username=username)
    if user and user.check_password(password):
        return user
    return None

@db_session
def list_all_users():
    """Return a list of all users (for administration)"""
    return select(u for u in User)[:]

@db_session
def delete_user(user_id):
    """Delete a user"""
    user = get_user(user_id)
    if user:
        user.delete()
        return True
    return False

# Patient-specific functions
@db_session
def get_patient_by_user_id(user_id):
    """Get patient record by user ID"""
    user = get_user(user_id)
    if user and user.role == 'patient':
        return Patient.get(user=user)
    return None

@db_session
def get_doctor_by_user_id(user_id):
    """Get doctor record by user ID"""
    user = get_user(user_id)
    if user and user.role == 'doctor':
        return Doctor.get(user=user)
    return None

# Glucose readings functions
@db_session
def add_glucose_reading(patient_id, value, is_before_meal, notes=None):
    """Add a new glucose reading for a patient"""
    patient = Patient[patient_id]
    if not patient:
        return False
    
    GlucoseReading(
        patient=patient,
        value=value,
        measurement_time=datetime.now(),
        is_before_meal=is_before_meal,
        notes=notes
    )
    return True

@db_session
def get_patient_glucose_readings(patient_id, days=30):
    """Get glucose readings for a patient in the last N days"""
    patient = Patient[patient_id]
    if not patient:
        return []
    
    since_date = datetime.now() - timedelta(days=days)
    return select(gr for gr in patient.glucose_readings 
                 if gr.measurement_time >= since_date).order_by(lambda gr: gr.measurement_time)[:]

# Therapy functions
@db_session
def add_therapy(patient_id, doctor_id, drug_name, daily_doses, dose_amount, dose_unit, instructions=None):
    """Add a new therapy prescribed by a doctor"""
    patient = Patient[patient_id]
    doctor = Doctor[doctor_id]
    
    if not patient or not doctor:
        return False
    
    Therapy(
        patient=patient,
        doctor=doctor,
        drug_name=drug_name,
        daily_doses=daily_doses,
        dose_amount=dose_amount,
        dose_unit=dose_unit,
        instructions=instructions,
        start_date=datetime.now()
    )
    return True

@db_session
def get_patient_active_therapies(patient_id):
    """Get all active therapies for a patient"""
    patient = Patient[patient_id]
    if not patient:
        return []
    
    return select(t for t in patient.therapies if t.is_active)[:]

# Medication intake functions
@db_session
def record_medication_intake(patient_id, therapy_id, dose_taken, notes=None):
    """Record that a patient took their medication"""
    patient = Patient[patient_id]
    therapy = Therapy[therapy_id]
    
    if not patient or not therapy:
        return False
    
    MedicationIntake(
        patient=patient,
        therapy=therapy,
        intake_time=datetime.now(),
        dose_taken=dose_taken,
        notes=notes
    )
    return True

# Symptom functions
@db_session
def add_symptom(patient_id, name, description=None, severity=None):
    """Add a symptom for a patient"""
    patient = Patient[patient_id]
    if not patient:
        return False
    
    Symptom(
        patient=patient,
        name=name,
        description=description,
        start_date=datetime.now(),
        severity=severity
    )
    return True

# Alert functions
@db_session
def create_alert(patient_id, alert_type, message, severity='medium', doctor_id=None):
    """Create an alert for glucose levels or medication compliance"""
    patient = Patient[patient_id]
    doctor = Doctor[doctor_id] if doctor_id else None
    
    if not patient:
        return False
    
    Alert(
        patient=patient,
        doctor=doctor,
        alert_type=alert_type,
        message=message,
        severity=severity,
        created_at=datetime.now()
    )
    return True

@db_session
def get_unread_alerts(doctor_id=None, patient_id=None):
    """Get unread alerts for a doctor or patient"""
    if doctor_id:
        doctor = Doctor[doctor_id]
        return select(a for a in doctor.alerts if not a.is_read)[:]
    elif patient_id:
        patient = Patient[patient_id]
        return select(a for a in patient.alerts if not a.is_read)[:]
    return []

# Alert checking functions
@db_session
def check_glucose_alerts(patient_id):
    """Check if patient has dangerous glucose levels and create alerts"""
    patient = Patient[patient_id]
    if not patient:
        return
    
    # Get recent glucose readings (last 24 hours)
    recent_readings = select(gr for gr in patient.glucose_readings 
                           if gr.measurement_time >= datetime.now() - timedelta(hours=24))[:]
    
    for reading in recent_readings:
        if reading.is_before_meal and (reading.value < 80 or reading.value > 130):
            severity = 'high' if reading.value < 70 or reading.value > 180 else 'medium'
            create_alert(
                patient_id, 
                'glucose_abnormal',
                f"Glucose level {reading.value} mg/dL before meal (normal: 80-130 mg/dL)",
                severity,
                patient.assigned_doctor.id if patient.assigned_doctor else None
            )
        elif not reading.is_before_meal and reading.value > 180:
            severity = 'high' if reading.value > 250 else 'medium'
            create_alert(
                patient_id,
                'glucose_abnormal', 
                f"Glucose level {reading.value} mg/dL after meal (should be <180 mg/dL)",
                severity,
                patient.assigned_doctor.id if patient.assigned_doctor else None
            )