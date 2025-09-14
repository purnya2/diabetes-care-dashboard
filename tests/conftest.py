# tests/conftest.py
"""
Configurazione globale per i test del backend del sistema di cura del diabete.
Imposta database di test isolato e fixtures comuni.
"""
import pytest
import os
import sys
from datetime import datetime, timedelta
from pony.orm import db_session, Database, Required, Optional, Set, PrimaryKey
from werkzeug.security import generate_password_hash

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.user import User, Patient, Doctor, GlucoseReading, Therapy, MedicationIntake, Alert, Symptom

@pytest.fixture(scope="function")
def test_db():
    """
    Crea un database SQLite in memoria isolato per ogni test.
    Garantisce che ogni test parta con uno stato pulito.
    """
    # Create new database instance for testing
    test_database = Database()
    
    # Bind entities to test database
    class TestUser(test_database.Entity):
        _table_ = 'User'
        username = Required(str, unique=True)
        password_hash = Required(str)
        is_active = Required(bool, default=True)
        role = Required(str)
        
        # Reverse relationships
        patient = Optional('TestPatient')
        doctor = Optional('TestDoctor')
        
        def check_password(self, password):
            from werkzeug.security import check_password_hash
            return check_password_hash(self.password_hash, password)
        
        def get_id(self):
            return str(self.id)
    
    class TestPatient(test_database.Entity):
        _table_ = 'Patient'
        user = Required('TestUser')
        assigned_doctor = Optional('TestDoctor')
        birth_date = Optional(datetime)
        diagnosis_date = Optional(datetime)
        diabetes_type = Optional(int)
        risk_factors = Optional(str)
        medical_history = Optional(str)
        comorbidities = Optional(str)
        
        # Reverse relationships
        glucose_readings = Set('TestGlucoseReading')
        therapies = Set('TestTherapy')
        medication_intakes = Set('TestMedicationIntake')
        alerts = Set('TestAlert')
    
    class TestDoctor(test_database.Entity):
        _table_ = 'Doctor'
        user = Required('TestUser')
        
        # Reverse relationships
        patients = Set('TestPatient')
        therapies = Set('TestTherapy')
        alerts = Set('TestAlert')
    
    class TestGlucoseReading(test_database.Entity):
        _table_ = 'GlucoseReading'
        patient = Required('TestPatient')
        value = Required(float)
        measurement_time = Required(datetime)
        is_before_meal = Required(bool)
        notes = Optional(str)
    
    class TestTherapy(test_database.Entity):
        _table_ = 'Therapy'
        patient = Required('TestPatient')
        doctor = Required('TestDoctor')
        drug_name = Required(str)
        daily_doses = Required(int)
        dose_amount = Required(float)
        dose_unit = Required(str)
        instructions = Optional(str)
        start_date = Required(datetime)
        end_date = Optional(datetime)
        is_active = Required(bool, default=True)
        
        # Reverse relationships
        medication_intakes = Set('TestMedicationIntake')
    
    class TestMedicationIntake(test_database.Entity):
        _table_ = 'MedicationIntake'
        patient = Required('TestPatient')
        therapy = Required('TestTherapy')
        intake_time = Required(datetime)
        dose_taken = Required(float)
        notes = Optional(str)
    
    class TestAlert(test_database.Entity):
        _table_ = 'Alert'
        patient = Required('TestPatient')
        doctor = Optional('TestDoctor')
        alert_type = Required(str)
        message = Required(str)
        severity = Required(str)
        created_at = Required(datetime)
        is_read = Required(bool, default=False)
        resolved_at = Optional(datetime)
    
    # Bind to in-memory SQLite database
    test_database.bind('sqlite', ':memory:')
    test_database.generate_mapping(create_tables=True)
    
    yield test_database
    
    # Cleanup
    test_database.rollback()
    test_database.disconnect()

@pytest.fixture
def sample_doctor(test_db):
    """Crea un dottore di esempio per i test"""
    # Note: This fixture should be used within a db_session in the test
    return {
        'username': 'test_doctor',
        'password_hash': generate_password_hash('testpass'),
        'role': 'doctor'
    }

@pytest.fixture
def sample_patient_data(test_db):
    """Fornisce dati per creare un paziente di esempio"""
    return {
        'username': 'test_patient',
        'password_hash': generate_password_hash('testpass'),
        'role': 'patient',
        'risk_factors': 'smoking, obesity',
        'medical_history': 'hypertension',
        'comorbidities': 'none'
    }

@pytest.fixture
def sample_therapy_data(test_db):
    """Fornisce dati per creare una terapia di esempio"""
    return {
        'drug_name': 'Metformin',
        'daily_doses': 2,
        'dose_amount': 500.0,
        'dose_unit': 'mg',
        'instructions': 'Take with meals',
        'start_date': datetime.now() - timedelta(days=30),
        'end_date': None,
        'is_active': True
    }

@pytest.fixture
def glucose_readings_data():
    """Dati di test per letture della glicemia"""
    return [
        {
            'value': 120.0,
            'is_before_meal': True,
            'measurement_time': datetime.now() - timedelta(hours=2),
            'notes': 'Before breakfast'
        },
        {
            'value': 180.0,
            'is_before_meal': False,
            'measurement_time': datetime.now() - timedelta(hours=1),
            'notes': 'After breakfast'
        },
        {
            'value': 250.0,  # High reading - should trigger alert
            'is_before_meal': False,
            'measurement_time': datetime.now(),
            'notes': 'High reading after meal'
        }
    ]

@pytest.fixture
def medication_intake_data():
    """Dati di test per assunzioni di farmaci"""
    return [
        {
            'intake_time': datetime.now() - timedelta(days=1),
            'dose_taken': 500.0,
            'notes': 'Taken with breakfast'
        },
        {
            'intake_time': datetime.now() - timedelta(days=2),
            'dose_taken': 500.0,
            'notes': 'Taken with dinner'
        }
    ]

'''
Questo file (conftest.py) contiene la configurazione globale per i test del backend.
Fornisce database di test isolato e fixtures per creare dati di test consistenti.
'''