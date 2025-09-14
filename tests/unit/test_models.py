# tests/unit/test_models.py
"""
Test unitari per i modelli del database del sistema di cura del diabete.
Testa entità User, Patient, Doctor e le loro relazioni.
"""
import pytest
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from pony.orm import db_session


class TestUserModel:
    """Test per il modello User"""
    
    def test_user_creation(self, test_db):
        """Test creazione utente base"""
        with db_session:
            user = test_db.TestUser(
                username='testuser',
                password_hash=generate_password_hash('testpass'),
                role='patient'
            )
            
            assert user.username == 'testuser'
            assert user.role == 'patient'
            assert user.is_active == True
            assert user.check_password('testpass') == True
            assert user.check_password('wrongpass') == False
    
    def test_user_unique_username(self, test_db):
        """Test che gli username siano unici"""
        with db_session:
            user1 = test_db.TestUser(
                username='duplicate',
                password_hash=generate_password_hash('pass1'),
                role='patient'
            )
            
            # Tentativo di creare utente con stesso username dovrebbe fallire
            with pytest.raises(Exception):  # Pony ORM dovrebbe lanciare eccezione
                user2 = test_db.TestUser(
                    username='duplicate',
                    password_hash=generate_password_hash('pass2'),
                    role='doctor'
                )
    
    def test_user_roles(self, test_db):
        """Test ruoli utente (patient, doctor)"""
        with db_session:
            patient_user = test_db.TestUser(
                username='patient_test',
                password_hash=generate_password_hash('pass'),
                role='patient'
            )
            
            doctor_user = test_db.TestUser(
                username='doctor_test',
                password_hash=generate_password_hash('pass'),
                role='doctor'
            )
            
            assert patient_user.role == 'patient'
            assert doctor_user.role == 'doctor'


class TestPatientModel:
    """Test per il modello Patient"""
    
    def test_patient_creation(self, test_db):
        """Test creazione paziente con validazione campi"""
        with db_session:
            # Crea prima il dottore
            doctor_user = test_db.TestUser(
                username='test_doctor',
                password_hash=generate_password_hash('testpass'),
                role='doctor'
            )
            doctor = test_db.TestDoctor(user=doctor_user)
            
            # Crea l'utente paziente
            patient_user = test_db.TestUser(
                username='test_patient',
                password_hash=generate_password_hash('testpass'),
                role='patient'
            )
            
            # Crea il paziente
            patient = test_db.TestPatient(
                user=patient_user,
                assigned_doctor=doctor,
                risk_factors='smoking, obesity',
                medical_history='hypertension',
                comorbidities='none'
            )
            
            assert patient.user.username == 'test_patient'
            assert patient.assigned_doctor == doctor
            assert patient.risk_factors == 'smoking, obesity'
            assert patient.medical_history == 'hypertension'
            assert patient.comorbidities == 'none'
    
    def test_patient_without_doctor(self, test_db):
        """Test paziente senza dottore assegnato"""
        with db_session:
            user = test_db.TestUser(
                username='patient_no_doctor',
                password_hash=generate_password_hash('pass'),
                role='patient'
            )
            
            patient = test_db.TestPatient(
                user=user,
                assigned_doctor=None
            )
            
            assert patient.assigned_doctor is None


class TestDoctorModel:
    """Test per il modello Doctor"""
    
    def test_doctor_creation(self, test_db):
        """Test creazione dottore"""
        with db_session:
            user = test_db.TestUser(
                username='doctor_test',
                password_hash=generate_password_hash('pass'),
                role='doctor'
            )
            
            doctor = test_db.TestDoctor(user=user)
            
            assert doctor.user.username == 'doctor_test'
            assert doctor.user.role == 'doctor'
    
    def test_doctor_patient_relationship(self, test_db):
        """Test relazione dottore-pazienti"""
        with db_session:
            # Crea dottore
            doctor_user = test_db.TestUser(
                username='doctor_rel',
                password_hash=generate_password_hash('pass'),
                role='doctor'
            )
            doctor = test_db.TestDoctor(user=doctor_user)
            
            # Crea pazienti
            patient1_user = test_db.TestUser(
                username='patient1_rel',
                password_hash=generate_password_hash('pass'),
                role='patient'
            )
            patient1 = test_db.TestPatient(user=patient1_user, assigned_doctor=doctor)
            
            patient2_user = test_db.TestUser(
                username='patient2_rel',
                password_hash=generate_password_hash('pass'),
                role='patient'
            )
            patient2 = test_db.TestPatient(user=patient2_user, assigned_doctor=doctor)
            
            # Verifica relazioni
            assert len(doctor.patients) == 2
            assert patient1 in doctor.patients
            assert patient2 in doctor.patients


class TestGlucoseReading:
    """Test per il modello GlucoseReading"""
    
    def test_glucose_reading_creation(self, test_db):
        """Test creazione lettura glicemica con validazione"""
        with db_session:
            # Setup complete entities
            doctor_user = test_db.TestUser(
                username='test_doctor',
                password_hash=generate_password_hash('testpass'),
                role='doctor'
            )
            doctor = test_db.TestDoctor(user=doctor_user)
            
            patient_user = test_db.TestUser(
                username='test_patient',
                password_hash=generate_password_hash('testpass'),
                role='patient'
            )
            patient = test_db.TestPatient(user=patient_user, assigned_doctor=doctor)
            
            reading = test_db.TestGlucoseReading(
                patient=patient,
                value=120.0,
                measurement_time=datetime.now(),
                is_before_meal=True,
                notes='Test reading'
            )
            
            assert reading.patient == patient
            assert reading.value == 120.0
            assert reading.is_before_meal == True
            assert reading.notes == 'Test reading'
    
    def test_glucose_reading_edge_values(self, test_db):
        """Test lettura glicemica con valori limite"""
        with db_session:
            # Setup entities
            doctor_user = test_db.TestUser(
                username='test_doctor',
                password_hash=generate_password_hash('testpass'),
                role='doctor'
            )
            doctor = test_db.TestDoctor(user=doctor_user)
            
            patient_user = test_db.TestUser(
                username='test_patient',
                password_hash=generate_password_hash('testpass'),
                role='patient'
            )
            patient = test_db.TestPatient(user=patient_user, assigned_doctor=doctor)
            
            # Test valore molto basso (ipoglicemia)
            low_reading = test_db.TestGlucoseReading(
                patient=patient,
                value=40.0,
                measurement_time=datetime.now(),
                is_before_meal=True,
                notes='Hypoglycemia episode'
            )
            
            # Test valore molto alto (iperglicemia)
            high_reading = test_db.TestGlucoseReading(
                patient=patient,
                value=400.0,
                measurement_time=datetime.now(),
                is_before_meal=False,
                notes='Hyperglycemia episode'
            )
            
            assert low_reading.value == 40.0
            assert high_reading.value == 400.0
class TestTherapyModel:
    """Test per il modello Therapy"""
    
    def test_therapy_creation(self, test_db):
        """Test creazione terapia"""
        with db_session:
            # Create test entities
            doctor_user = test_db.TestUser(
                username='test_doctor',
                password_hash=generate_password_hash('testpass'),
                role='doctor'
            )
            doctor = test_db.TestDoctor(user=doctor_user)
            
            patient_user = test_db.TestUser(
                username='test_patient',
                password_hash=generate_password_hash('testpass'),
                role='patient'
            )
            patient = test_db.TestPatient(user=patient_user, assigned_doctor=doctor)
            
            therapy = test_db.TestTherapy(
                patient=patient,
                doctor=doctor,
                drug_name='Metformin',
                daily_doses=2,
                dose_amount=500.0,
                dose_unit='mg',
                instructions='Take with meals',
                start_date=datetime.now()
            )
            
            assert therapy.patient == patient
            assert therapy.doctor == doctor
            assert therapy.drug_name == 'Metformin'
            assert therapy.daily_doses == 2
            assert therapy.dose_amount == 500.0
            assert therapy.dose_unit == 'mg'
            assert therapy.is_active == True
    
    def test_therapy_activation_status(self, test_db):
        """Test stato attivazione terapia"""
        with db_session:
            # Create test entities
            doctor_user = test_db.TestUser(
                username='test_doctor_therapy',
                password_hash=generate_password_hash('testpass'),
                role='doctor'
            )
            doctor = test_db.TestDoctor(user=doctor_user)
            
            patient_user = test_db.TestUser(
                username='test_patient_therapy',
                password_hash=generate_password_hash('testpass'),
                role='patient'
            )
            patient = test_db.TestPatient(user=patient_user, assigned_doctor=doctor)
            
            # Terapia attiva
            active_therapy = test_db.TestTherapy(
                patient=patient,
                doctor=doctor,
                drug_name='Insulin',
                daily_doses=3,
                dose_amount=10.0,
                dose_unit='units',
                start_date=datetime.now(),
                is_active=True
            )
            
            # Terapia non attiva
            inactive_therapy = test_db.TestTherapy(
                patient=patient,
                doctor=doctor,
                drug_name='Old Medicine',
                daily_doses=1,
                dose_amount=100.0,
                dose_unit='mg',
                start_date=datetime.now() - timedelta(days=30),
                end_date=datetime.now() - timedelta(days=1),
                is_active=False
            )
            
            assert active_therapy.is_active == True
            assert inactive_therapy.is_active == False


class TestMedicationIntake:
    """Test per il modello MedicationIntake"""
    
    def test_medication_intake_creation(self, test_db):
        """Test registrazione assunzione farmaco"""
        with db_session:
            # Create test entities
            doctor_user = test_db.TestUser(
                username='test_doctor_intake',
                password_hash=generate_password_hash('testpass'),
                role='doctor'
            )
            doctor = test_db.TestDoctor(user=doctor_user)
            
            patient_user = test_db.TestUser(
                username='test_patient_intake',
                password_hash=generate_password_hash('testpass'),
                role='patient'
            )
            patient = test_db.TestPatient(user=patient_user, assigned_doctor=doctor)
            
            therapy = test_db.TestTherapy(
                patient=patient,
                doctor=doctor,
                drug_name='Metformin',
                daily_doses=2,
                dose_amount=500.0,
                dose_unit='mg',
                instructions='Take with meals',
                start_date=datetime.now()
            )
            
            intake = test_db.TestMedicationIntake(
                patient=patient,
                therapy=therapy,
                intake_time=datetime.now(),
                dose_taken=500.0,
                notes='Taken with breakfast'
            )
            
            assert intake.patient == patient
            assert intake.therapy == therapy
            assert intake.dose_taken == 500.0
            assert intake.notes == 'Taken with breakfast'


class TestAlertModel:
    """Test per il modello Alert"""
    
    def test_alert_creation(self, test_db):
        """Test creazione alert"""
        with db_session:
            # Create test entities
            doctor_user = test_db.TestUser(
                username='test_doctor_alert',
                password_hash=generate_password_hash('testpass'),
                role='doctor'
            )
            doctor = test_db.TestDoctor(user=doctor_user)
            
            patient_user = test_db.TestUser(
                username='test_patient_alert',
                password_hash=generate_password_hash('testpass'),
                role='patient'
            )
            patient = test_db.TestPatient(user=patient_user, assigned_doctor=doctor)
            
            alert = test_db.TestAlert(
                patient=patient,
                doctor=doctor,
                alert_type='glucose_high',
                message='High glucose level detected',
                severity='high',
                created_at=datetime.now()
            )
            
            assert alert.patient == patient
            assert alert.doctor == doctor
            assert alert.alert_type == 'glucose_high'
            assert alert.severity == 'high'
            assert alert.is_read == False
            assert alert.resolved_at is None
    
    def test_alert_severities(self, test_db):
        """Test diversi livelli di severità degli alert"""
        with db_session:
            # Create test entities
            doctor_user = test_db.TestUser(
                username='test_doctor_severity',
                password_hash=generate_password_hash('testpass'),
                role='doctor'
            )
            doctor = test_db.TestDoctor(user=doctor_user)
            
            patient_user = test_db.TestUser(
                username='test_patient_severity',
                password_hash=generate_password_hash('testpass'),
                role='patient'
            )
            patient = test_db.TestPatient(user=patient_user, assigned_doctor=doctor)
            
            severities = ['low', 'medium', 'high']
            
            for i, severity in enumerate(severities):
                alert = test_db.TestAlert(
                    patient=patient,
                    doctor=doctor,
                    alert_type='test_alert',
                    message=f'{severity} severity alert',
                    severity=severity,
                    created_at=datetime.now()
                )
                assert alert.severity == severity
    
    def test_alert_read_status(self, test_db):
        """Test stato lettura degli alert"""
        with db_session:
            # Create test entities
            doctor_user = test_db.TestUser(
                username='test_doctor_read',
                password_hash=generate_password_hash('testpass'),
                role='doctor'
            )
            doctor = test_db.TestDoctor(user=doctor_user)
            
            patient_user = test_db.TestUser(
                username='test_patient_read',
                password_hash=generate_password_hash('testpass'),
                role='patient'
            )
            patient = test_db.TestPatient(user=patient_user, assigned_doctor=doctor)
            
            alert = test_db.TestAlert(
                patient=patient,
                doctor=doctor,
                alert_type='test_alert',
                message='Test message',
                severity='medium',
                created_at=datetime.now(),
                is_read=True,
                resolved_at=datetime.now()
            )
            
            assert alert.is_read == True
            assert alert.resolved_at is not None

'''
Questo file (test_models.py) contiene test unitari per tutti i modelli del database.
Verifica la creazione delle entità, le relazioni e i vincoli di integrità dei dati.
'''