# tests/test_basic.py
"""
Basic test to verify the testing infrastructure is working.
This test validates that the database setup and basic functionality works.
"""
import pytest
from datetime import datetime, timedelta
from pony.orm import db_session
from werkzeug.security import generate_password_hash

def test_basic_database_setup(test_db):
    """Test che il database di test funzioni correttamente"""
    with db_session:
        # Create a basic user
        user = test_db.TestUser(
            username='test_user',
            password_hash=generate_password_hash('password123'),
            role='patient'
        )
        
        assert user.username == 'test_user'
        assert user.role == 'patient'
        assert user.is_active == True

def test_patient_doctor_relationship(test_db):
    """Test relazione paziente-dottore"""
    with db_session:
        # Create doctor
        doctor_user = test_db.TestUser(
            username='dr_smith',
            password_hash=generate_password_hash('docpass'),
            role='doctor'
        )
        doctor = test_db.TestDoctor(user=doctor_user)
        
        # Create patient
        patient_user = test_db.TestUser(
            username='patient_john',
            password_hash=generate_password_hash('patpass'),
            role='patient'
        )
        patient = test_db.TestPatient(
            user=patient_user,
            assigned_doctor=doctor
        )
        
        # Verify relationships
        assert patient.assigned_doctor == doctor
        assert patient in doctor.patients

def test_glucose_reading_creation(test_db):
    """Test creazione lettura glicemica"""
    with db_session:
        # Setup entities
        doctor_user = test_db.TestUser(
            username='doctor1',
            password_hash=generate_password_hash('pass'),
            role='doctor'
        )
        doctor = test_db.TestDoctor(user=doctor_user)
        
        patient_user = test_db.TestUser(
            username='patient1',
            password_hash=generate_password_hash('pass'),
            role='patient'
        )
        patient = test_db.TestPatient(user=patient_user, assigned_doctor=doctor)
        
        # Create glucose reading
        reading = test_db.TestGlucoseReading(
            patient=patient,
            value=150.0,
            measurement_time=datetime.now(),
            is_before_meal=True,
            notes='Morning reading'
        )
        
        assert reading.value == 150.0
        assert reading.patient == patient
        assert reading.is_before_meal == True

def test_therapy_and_intake(test_db):
    """Test completo: terapia e assunzione farmaci"""
    with db_session:
        # Setup entities
        doctor_user = test_db.TestUser(
            username='doctor2',
            password_hash=generate_password_hash('pass'),
            role='doctor'
        )
        doctor = test_db.TestDoctor(user=doctor_user)
        
        patient_user = test_db.TestUser(
            username='patient2',
            password_hash=generate_password_hash('pass'),
            role='patient'
        )
        patient = test_db.TestPatient(user=patient_user, assigned_doctor=doctor)
        
        # Create therapy
        therapy = test_db.TestTherapy(
            patient=patient,
            doctor=doctor,
            drug_name='Metformin',
            daily_doses=2,
            dose_amount=500.0,
            dose_unit='mg',
            instructions='Take with meals',
            start_date=datetime.now() - timedelta(days=7)
        )
        
        # Create medication intake
        intake = test_db.TestMedicationIntake(
            patient=patient,
            therapy=therapy,
            intake_time=datetime.now(),
            dose_taken=500.0,
            notes='Morning dose'
        )
        
        assert therapy.patient == patient
        assert therapy.doctor == doctor
        assert intake.therapy == therapy
        assert intake.dose_taken == 500.0

def test_alert_creation(test_db):
    """Test creazione alert"""
    with db_session:
        # Setup entities
        doctor_user = test_db.TestUser(
            username='doctor3',
            password_hash=generate_password_hash('pass'),
            role='doctor'
        )
        doctor = test_db.TestDoctor(user=doctor_user)
        
        patient_user = test_db.TestUser(
            username='patient3',
            password_hash=generate_password_hash('pass'),
            role='patient'
        )
        patient = test_db.TestPatient(user=patient_user, assigned_doctor=doctor)
        
        # Create alert
        alert = test_db.TestAlert(
            patient=patient,
            doctor=doctor,
            alert_type='glucose_high',
            message='High glucose reading detected',
            severity='high',
            created_at=datetime.now()
        )
        
        assert alert.patient == patient
        assert alert.doctor == doctor
        assert alert.severity == 'high'
        assert alert.is_read == False  # Default value