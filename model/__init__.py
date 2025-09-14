# model/__init__.py
# Import and configure database
from model.database import db, configure_db

# Import entity classes
from model.user import User, Patient, Doctor, GlucoseReading, Symptom, Therapy, MedicationIntake, Alert

# Import all operations for external use
from model.operations import (
    initialize_db, get_user, get_user_by_username, add_user, validate_user,
    list_all_users, delete_user, get_patient_by_user_id, get_doctor_by_user_id,
    add_glucose_reading, get_patient_glucose_readings, add_therapy, 
    get_patient_active_therapies, record_medication_intake, add_symptom,
    create_alert, get_unread_alerts, check_glucose_alerts,
    check_medication_compliance, check_all_patients_compliance, 
    get_therapy_compliance_status, check_glucose_thresholds_and_alert,
    clear_compliance_alerts_for_patient, check_and_clear_compliance_alerts,
    update_patient_info
)

# Configure the database when the module is imported
configure_db()

# Initialize the database with default users
initialize_db()

# Export all necessary functions for diabetes care system
__all__ = [
    'db', 'User', 'Patient', 'Doctor', 'GlucoseReading', 'Symptom', 'Therapy', 'MedicationIntake', 'Alert',
    'initialize_db', 'get_user', 'get_user_by_username', 'add_user', 'validate_user',
    'list_all_users', 'delete_user', 'get_patient_by_user_id', 'get_doctor_by_user_id',
    'add_glucose_reading', 'get_patient_glucose_readings', 'add_therapy',
    'get_patient_active_therapies', 'record_medication_intake', 'add_symptom',
    'create_alert', 'get_unread_alerts', 'check_glucose_alerts',
    'check_medication_compliance', 'check_all_patients_compliance', 
    'get_therapy_compliance_status', 'check_glucose_thresholds_and_alert',
    'clear_compliance_alerts_for_patient', 'check_and_clear_compliance_alerts',
    'update_patient_info'
]

'''
    Questo file (__init__.py) del modulo model configura e espone tutte le funzionalità del database.
    Importa entità, operazioni e inizializza il sistema di persistenza per l'app diabetologica.
'''