# model/user.py
from pony.orm import Required, Optional, PrimaryKey, Set
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .database import db
from datetime import datetime

# Define the User entity
class User(db.Entity, UserMixin):
    username = Required(str, unique=True)
    password_hash = Required(str)
    is_active = Required(bool, default=True)
    role = Required(str)  # 'patient', 'doctor'
    
    # Relationships
    patient_profile = Optional('Patient', reverse='user')
    doctor_profile = Optional('Doctor', reverse='user')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.id)

    def is_patient(self):
        return self.role == 'patient'

    def is_doctor(self):
        return self.role == 'doctor'

class Patient(db.Entity):
    user = Required(User, reverse='patient_profile')
    assigned_doctor = Optional('Doctor', reverse='patients')
    # Patient information
    risk_factors = Optional(str)  # smoking, alcohol, drugs, obesity
    medical_history = Optional(str)  # previous pathologies
    comorbidities = Optional(str)  # hypertension, etc.
    notes = Optional(str)  # doctor's clinical notes
    
    # Relationships
    glucose_readings = Set('GlucoseReading', reverse='patient')
    symptoms = Set('Symptom', reverse='patient')
    medication_intakes = Set('MedicationIntake', reverse='patient')
    therapies = Set('Therapy', reverse='patient')
    alerts = Set('Alert', reverse='patient')

class Doctor(db.Entity):
    user = Required(User, reverse='doctor_profile')
    patients = Set(Patient, reverse='assigned_doctor')
    prescribed_therapies = Set('Therapy', reverse='doctor')
    alerts = Set('Alert', reverse='doctor')

class GlucoseReading(db.Entity):
    patient = Required(Patient, reverse='glucose_readings')
    value = Required(float)  # mg/dL
    measurement_time = Required(datetime)
    is_before_meal = Required(bool)  # True if before meal, False if after
    notes = Optional(str)

class Symptom(db.Entity):
    patient = Required(Patient, reverse='symptoms')
    name = Required(str)  # fatigue, nausea, headache, etc.
    description = Optional(str)
    start_date = Required(datetime)
    end_date = Optional(datetime)
    severity = Optional(str)  # mild, moderate, severe

class Therapy(db.Entity):
    patient = Required(Patient, reverse='therapies')
    doctor = Required(Doctor, reverse='prescribed_therapies')
    drug_name = Required(str)
    daily_doses = Required(int)  # number of doses per day
    dose_amount = Required(float)
    dose_unit = Required(str)  # mg, IU, etc.
    instructions = Optional(str)  # after meals, away from meals, etc.
    start_date = Required(datetime)
    end_date = Optional(datetime)
    is_active = Required(bool, default=True)
    medication_intakes = Set('MedicationIntake', reverse='therapy')

class MedicationIntake(db.Entity):
    patient = Required(Patient, reverse='medication_intakes')
    therapy = Required(Therapy, reverse='medication_intakes')
    intake_time = Required(datetime)
    dose_taken = Required(float)
    notes = Optional(str)

class Alert(db.Entity):
    patient = Required(Patient, reverse='alerts')
    doctor = Optional(Doctor, reverse='alerts')
    alert_type = Required(str)  # 'glucose_high', 'glucose_low', 'medication_missed', 'compliance_issue'
    message = Required(str)
    severity = Required(str)  # 'low', 'medium', 'high'
    created_at = Required(datetime)
    is_read = Required(bool, default=False)
    resolved_at = Optional(datetime)

'''
    Questo file (user.py) definisce i modelli del database per gli utenti del sistema.
    Contiene le classi User (utente base), Patient (paziente) e Doctor (dottore) con 
    tutte le loro proprietà e relazioni per gestire il sistema di telemedicina diabetica.
'''