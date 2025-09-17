# model/operations.py
from pony.orm import db_session, select, delete, commit, count, desc
from werkzeug.security import generate_password_hash
from datetime import date, datetime, timedelta

from model.user import User, Patient, Doctor, GlucoseReading, Symptom, Therapy, MedicationIntake, Alert

# Database initialization
@db_session
def initialize_db():

    # here we create our dummy data
    if User.select().count() == 0:
        # Create multiple doctors
        dr_smith_user = User(username='dr_smith', password_hash=generate_password_hash('doctorpass'), role='doctor')
        dr_smith = Doctor(user=dr_smith_user)

        dr_johnson_user = User(username='dr_johnson', password_hash=generate_password_hash('doctorpass'), role='doctor')
        dr_johnson = Doctor(user=dr_johnson_user)

        dr_garcia_user = User(username='dr_garcia', password_hash=generate_password_hash('doctorpass'), role='doctor')
        dr_garcia = Doctor(user=dr_garcia_user)

        # Create multiple patients with different conditions
        # Patient 1: Well-controlled diabetes
        patient1_user = User(username='patient1', password_hash=generate_password_hash('patientpass'), role='patient')
        patient1 = Patient(user=patient1_user, assigned_doctor=dr_smith)

        # Patient 2: Poorly controlled diabetes with alerts
        patient2_user = User(username='mario_rossi', password_hash=generate_password_hash('patientpass'), role='patient')
        patient2 = Patient(user=patient2_user, assigned_doctor=dr_smith)

        # Patient 3: Newly diagnosed
        patient3_user = User(username='anna_verdi', password_hash=generate_password_hash('patientpass'), role='patient')
        patient3 = Patient(user=patient3_user, assigned_doctor=dr_johnson)

        # Patient 4: Type 1 diabetes with insulin
        patient4_user = User(username='luca_bianchi', password_hash=generate_password_hash('patientpass'), role='patient')
        patient4 = Patient(user=patient4_user, assigned_doctor=dr_garcia)

        # Patient 5: Gestational diabetes
        patient5_user = User(username='giulia_ferrari', password_hash=generate_password_hash('patientpass'), role='patient')
        patient5 = Patient(user=patient5_user, assigned_doctor=dr_johnson)

        # Create comprehensive therapies for each patient
        # Patient 1 therapies (well-controlled)
        Therapy(
            patient=patient1,
            doctor=dr_smith,
            drug_name="Metformin",
            daily_doses=2,
            dose_amount=500,
            dose_unit="mg",
            instructions="Take with meals, morning and evening",
            start_date=datetime.now() - timedelta(days=90)
        )

        # Patient 2 therapies (multiple medications)
        Therapy(
            patient=patient2,
            doctor=dr_smith,
            drug_name="Metformin",
            daily_doses=2,
            dose_amount=1000,
            dose_unit="mg",
            instructions="Take with breakfast and dinner",
            start_date=datetime.now() - timedelta(days=180)
        )

        Therapy(
            patient=patient2,
            doctor=dr_smith,
            drug_name="Glipizide",
            daily_doses=2,
            dose_amount=5,
            dose_unit="mg",
            instructions="Take 30 minutes before meals",
            start_date=datetime.now() - timedelta(days=60)
        )

        # Patient 3 therapies (newly diagnosed - lifestyle + metformin)
        Therapy(
            patient=patient3,
            doctor=dr_johnson,
            drug_name="Metformin",
            daily_doses=1,
            dose_amount=500,
            dose_unit="mg",
            instructions="Take with dinner, increase to twice daily after 2 weeks",
            start_date=datetime.now() - timedelta(days=14)
        )

        # Patient 4 therapies (Type 1 - insulin regimen)
        Therapy(
            patient=patient4,
            doctor=dr_garcia,
            drug_name="Insulin Glargine (Lantus)",
            daily_doses=1,
            dose_amount=20,
            dose_unit="units",
            instructions="Inject once daily at bedtime",
            start_date=datetime.now() - timedelta(days=365)
        )

        Therapy(
            patient=patient4,
            doctor=dr_garcia,
            drug_name="Insulin Lispro (Humalog)",
            daily_doses=3,
            dose_amount=8,
            dose_unit="units",
            instructions="Inject before each meal, adjust based on carb counting",
            start_date=datetime.now() - timedelta(days=365)
        )

        # Patient 5 therapies (gestational diabetes)
        Therapy(
            patient=patient5,
            doctor=dr_johnson,
            drug_name="Insulin NPH",
            daily_doses=2,
            dose_amount=10,
            dose_unit="units",
            instructions="Morning and evening doses, monitor closely",
            start_date=datetime.now() - timedelta(days=30)
        )

        # Create glucose readings with different patterns
        # Patient 1: Good control (mostly normal readings)
        for i in range(21):  # 3 weeks of data
            day_offset = timedelta(days=i)
            # Morning reading (before breakfast)
            GlucoseReading(
                patient=patient1,
                value=85 + (i % 10) * 2,  # 85-105 range
                measurement_time=datetime.now() - day_offset + timedelta(hours=7),
                is_before_meal=True,
                notes="Before breakfast" if i % 7 == 0 else ""
            )
            # Evening reading (after dinner)
            GlucoseReading(
                patient=patient1,
                value=140 + (i % 8) * 3,  # 140-165 range
                measurement_time=datetime.now() - day_offset + timedelta(hours=20),
                is_before_meal=False,
                notes="2 hours after dinner" if i % 7 == 0 else ""
            )

        # Patient 2: Poor control (high readings, some dangerous)
        for i in range(14):  # 2 weeks of data
            day_offset = timedelta(days=i)
            # Morning reading (often high)
            morning_value = 160 + (i % 15) * 4  # 160-220 range
            GlucoseReading(
                patient=patient2,
                value=morning_value,
                measurement_time=datetime.now() - day_offset + timedelta(hours=7),
                is_before_meal=True,
                notes="Feeling thirsty" if morning_value > 200 else ""
            )
            # Evening reading (very high)
            evening_value = 200 + (i % 12) * 5  # 200-255 range
            GlucoseReading(
                patient=patient2,
                value=evening_value,
                measurement_time=datetime.now() - day_offset + timedelta(hours=20),
                is_before_meal=False,
                notes="Had large meal" if evening_value > 240 else ""
            )

        # Patient 3: Newly diagnosed (improving trend)
        for i in range(14):  # 2 weeks since diagnosis
            day_offset = timedelta(days=i)
            # Improving trend from high to better controlled
            trend_improvement = max(0, 30 - i * 2)  # Decreasing adjustment
            morning_value = 140 + trend_improvement + (i % 5) * 2
            GlucoseReading(
                patient=patient3,
                value=morning_value,
                measurement_time=datetime.now() - day_offset + timedelta(hours=8),
                is_before_meal=True,
                notes="Learning to manage diet" if i < 3 else ""
            )

        # Patient 4: Type 1 with some variability
        for i in range(30):  # 1 month of data
            day_offset = timedelta(days=i)
            # More variable readings typical of Type 1
            morning_value = 90 + (i % 20) * 3  # 90-150 range
            GlucoseReading(
                patient=patient4,
                value=morning_value,
                measurement_time=datetime.now() - day_offset + timedelta(hours=7),
                is_before_meal=True,
                notes="Adjusted insulin dose" if morning_value > 140 else ""
            )
            # Post-meal readings
            postmeal_value = 120 + (i % 25) * 4  # 120-220 range
            GlucoseReading(
                patient=patient4,
                value=postmeal_value,
                measurement_time=datetime.now() - day_offset + timedelta(hours=14),
                is_before_meal=False,
                notes="Carb counting: 45g" if i % 10 == 0 else ""
            )

        # Patient 5: Gestational diabetes (moderate control)
        for i in range(30):  # 1 month of monitoring
            day_offset = timedelta(days=i)
            morning_value = 95 + (i % 12) * 2  # 95-120 range
            GlucoseReading(
                patient=patient5,
                value=morning_value,
                measurement_time=datetime.now() - day_offset + timedelta(hours=8),
                is_before_meal=True,
                notes="Pregnancy week " + str(28 + i//7) if i % 7 == 0 else ""
            )


        # Add symptoms
        # Patient 2: Multiple symptoms due to poor control
        Symptom(
            patient=patient2,
            name="Excessive thirst",
            description="Drinking water frequently throughout the day",
            start_date=datetime.now() - timedelta(days=10),
            severity="medium"
        )
        # Patient 2: Multiple symptoms due to poor control
        Symptom(
            patient=patient2,
            name="Excessive thirst",
            description="Drinking water frequently throughout the day",
            start_date=datetime.now() - timedelta(days=10),
            severity="medium"
        )

        Symptom(
            patient=patient2,
            name="Frequent urination",
            description="Waking up multiple times at night",
            start_date=datetime.now() - timedelta(days=8),
            severity="medium"
        )

        Symptom(
            patient=patient2,
            name="Fatigue",
            description="Feeling tired after meals",
            start_date=datetime.now() - timedelta(days=5),
            severity="high"
        )

        # Patient 3: Initial symptoms (improving)
        Symptom(
            patient=patient3,
            name="Blurred vision",
            description="Difficulty focusing, especially in the morning",
            start_date=datetime.now() - timedelta(days=14),
            severity="low"
        )

        # Patient 4: Hypoglycemia episode
        Symptom(
            patient=patient4,
            name="Hypoglycemia",
            description="Shakiness and sweating after exercise",
            start_date=datetime.now() - timedelta(days=3),
            severity="high"
        )

        # Create alerts based on the data
        # High glucose alerts for Patient 2
        Alert(
            patient=patient2,
            doctor=dr_smith,
            alert_type='glucose_high',
            message="Glucose level 245 mg/dL after meal - immediate attention needed",
            severity='high',
            created_at=datetime.now() - timedelta(hours=6),
            is_read=False
        )

        Alert(
            patient=patient2,
            doctor=dr_smith,
            alert_type='compliance_issue',
            message="Patient missed 3 medication doses this week",
            severity='medium',
            created_at=datetime.now() - timedelta(days=1),
            is_read=False
        )

        # Hypoglycemia alert for Patient 4
        Alert(
            patient=patient4,
            doctor=dr_garcia,
            alert_type='glucose_low',
            message="Patient reported hypoglycemia episode after exercise",
            severity='high',
            created_at=datetime.now() - timedelta(days=3),
            is_read=True,
            resolved_at=datetime.now() - timedelta(days=2)
        )

        # Follow-up alert for Patient 3
        Alert(
            patient=patient3,
            doctor=dr_johnson,
            alert_type='follow_up',
            message="2-week follow-up due for newly diagnosed patient",
            severity='low',
            created_at=datetime.now() - timedelta(hours=12),
            is_read=False
        )

        # Pregnancy monitoring alert for Patient 5
        Alert(
            patient=patient5,
            doctor=dr_johnson,
            alert_type='pregnancy_monitoring',
            message="Weekly glucose monitoring due for gestational diabetes",
            severity='medium',
            created_at=datetime.now() - timedelta(hours=24),
            is_read=False
        )

# User management functions
@db_session
def get_user(user_id):
    """Get a user by ID"""
    try:
        return User[int(user_id)]
    except (ValueError, TypeError):
        return None
    except Exception:
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
    return list(User.select())

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

@db_session
def update_patient_info(patient_id, risk_factors=None, medical_history=None, comorbidities=None, notes=None):
    """Update patient medical information"""
    try:
        patient = Patient[patient_id]
        if not patient:
            return False

        if risk_factors is not None:
            patient.risk_factors = risk_factors
        if medical_history is not None:
            patient.medical_history = medical_history
        if comorbidities is not None:
            patient.comorbidities = comorbidities
        if notes is not None:
            patient.notes = notes
        
        return True
    except Exception as e:
        print(f"Error updating patient info: {e}")
        return False

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
        notes=notes or ""
    )

    # Check glucose thresholds and create alerts for doctor
    check_glucose_thresholds_and_alert(patient_id)
    
    # Also check medication compliance (glucose readings might indicate missed medications)
    check_medication_compliance(patient_id)
    
    return True

@db_session
def get_patient_glucose_readings(patient_id, days=30):
    """Get glucose readings for a patient in the last N days"""
    patient = Patient[patient_id]
    if not patient:
        return []

    since_date = datetime.now() - timedelta(days=days)

    # Use simple iteration to avoid Pony ORM decompiler issues
    readings = []
    for reading in patient.glucose_readings:
        if reading.measurement_time >= since_date:
            readings.append(reading)

    # Sort by measurement time
    readings.sort(key=lambda gr: gr.measurement_time)
    return readings

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

    # Use simple iteration to avoid Pony ORM decompiler issues
    active_therapies = []
    for therapy in patient.therapies:
        if therapy.is_active:
            active_therapies.append(therapy)

    return active_therapies

# Medication intake functions
@db_session
def record_medication_intake(patient_id, therapy_id, dose_taken, notes=None, intake_datetime=None):
    """Record that a patient took their medication"""
    patient = Patient[patient_id]
    therapy = Therapy[therapy_id]

    if not patient or not therapy:
        return False

    # Use provided datetime or current time
    if intake_datetime is None:
        intake_datetime = datetime.now()

    MedicationIntake(
        patient=patient,
        therapy=therapy,
        intake_time=intake_datetime,
        dose_taken=dose_taken,
        notes=notes or ""
    )

    # Check medication compliance after recording intake
    check_medication_compliance(patient_id)

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
def alert_exists_recent(patient_id, alert_type, doctor_id=None, hours=24):
    """Check if a similar alert exists in the last N hours to avoid duplicates"""
    patient = Patient[patient_id]
    if not patient:
        return False
    
    since_time = datetime.now() - timedelta(hours=hours)
    
    # Split the complex query into simpler parts to avoid decompilation issues
    recent_alerts = select(a for a in patient.alerts 
                          if a.alert_type == alert_type 
                          and a.created_at >= since_time
                          and not a.is_read)[:]
    
    # Filter by doctor separately to avoid complex query conditions
    for alert in recent_alerts:
        if doctor_id:
            if alert.doctor and alert.doctor.id == doctor_id:
                return True
        else:
            if alert.doctor is None:
                return True
    
    return False

@db_session
def create_alert(patient_id, alert_type, message, severity='medium', doctor_id=None):
    """Create an alert for glucose levels or medication compliance"""
    try:
        patient = Patient.get(id=patient_id)
        if not patient:
            print(f"Patient with id {patient_id} not found")
            return False

        doctor = None
        if doctor_id:
            doctor = Doctor.get(id=doctor_id)
            if not doctor:
                print(f"Doctor with id {doctor_id} not found")

        Alert(
            patient=patient,
            doctor=doctor,
            alert_type=alert_type,
            message=message,
            severity=severity,
            created_at=datetime.now()
        )
        return True
    except Exception as e:
        print(f"Error creating alert: {e}")
        return False

@db_session
def create_doctor_alert(doctor_id, patient_id, alert_type, message, severity='medium'):
    """Create an alert primarily for a doctor about a patient"""
    try:
        doctor = Doctor.get(id=doctor_id)
        patient = Patient.get(id=patient_id)

        if not doctor:
            print(f"Doctor with id {doctor_id} not found")
            return False
        if not patient:
            print(f"Patient with id {patient_id} not found")
            return False

        # Create alert associated with patient but intended for doctor
        Alert(
            patient=patient,
            doctor=doctor,
            alert_type=alert_type,
            message=message,
            severity=severity,
            created_at=datetime.now()
        )
        return True
    except Exception as e:
        print(f"Error creating doctor alert: {e}")
        return False

@db_session
def get_unread_alerts(doctor_id=None, patient_id=None):
    """Get unread alerts for a doctor or patient, ordered by creation date (most recent first)"""
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
    recent_readings = []
    cutoff_time = datetime.now() - timedelta(hours=24)
    for reading in patient.glucose_readings:
        if reading.measurement_time >= cutoff_time:
            recent_readings.append(reading)

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

# Medication compliance functions
@db_session
def check_medication_compliance(patient_id):
    """Check if patient is compliant with medication intake and create alerts if needed"""
    try:
        patient = Patient.get(id=patient_id)
        if not patient:
            return

        # Get all active therapies for the patient
        active_therapies = []
        for therapy in patient.therapies:
            if therapy.is_active:
                active_therapies.append(therapy)

        if not active_therapies:
            return

        current_date = datetime.now().date()

        for therapy in active_therapies:
            # Check last 3 days for each therapy
            missing_days = 0
            consecutive_missing_days = 0

            for i in range(3):  # Check last 3 days
                check_date = current_date - timedelta(days=i)

                # Get expected intakes for this day (based on daily_doses)
                expected_intakes = therapy.daily_doses

                # Get actual intakes for this day
                actual_intakes = 0
                for mi in therapy.medication_intakes:
                    if mi.intake_time.date() == check_date:
                        actual_intakes += 1

                # Check if patient is missing doses for this day
                if actual_intakes < expected_intakes:
                    missing_days += 1
                    if i == 0:  # Most recent day
                        consecutive_missing_days += 1
                    elif consecutive_missing_days == i:  # Consecutive missing
                        consecutive_missing_days += 1

            # Create alerts based on missing patterns
            if consecutive_missing_days >= 3:
                # Alert for both patient and doctor after 3 consecutive days
                create_alert(
                    patient_id,
                    'medication_compliance',
                    f"You haven't recorded taking {therapy.drug_name} for {consecutive_missing_days} consecutive days. Please remember to take your medication as prescribed.",
                    'high'
                )

                if patient.assigned_doctor:
                    create_doctor_alert(
                        patient.assigned_doctor.id,
                        patient_id,
                        'patient_non_compliance',
                        f"Patient {patient.user.username} has not recorded taking {therapy.drug_name} for {consecutive_missing_days} consecutive days.",
                        'high'
                    )

            elif missing_days >= 2:
                # Reminder alert for patient
                create_alert(
                    patient_id,
                    'medication_reminder',
                    f"Reminder: Please remember to record your {therapy.drug_name} intake. You've missed recording for {missing_days} days in the last 3 days.",
                    'medium'
                )
    except Exception as e:
        print(f"Error checking compliance for patient {patient_id}: {e}")
        return

@db_session
def check_all_patients_compliance():
    """Check medication compliance for all patients - to be called periodically"""
    try:
        # First, clear all existing compliance alerts to prevent duplicates
        clear_all_compliance_alerts()
        
        patients = select(p for p in Patient)[:]
        
        for patient in patients:
            try:
                check_medication_compliance(patient.id)
            except Exception as e:
                print(f"Error checking compliance for patient {patient.id}: {e}")
                
    except Exception as e:
        print(f"Error in check_all_patients_compliance: {e}")
        # If no patients exist yet, that's fine
        if "no such table" in str(e) or "ObjectNotFound" in str(e):
            print("No patients found - this is normal for a new database")
        else:
            raise

@db_session
def get_therapy_compliance_status(patient_id, days=7):
    """Get detailed compliance status for a patient's therapies over specified days"""
    patient = Patient[patient_id]
    if not patient:
        return []

    # Use simple iteration to avoid Pony ORM decompiler issues
    active_therapies = []
    for therapy in patient.therapies:
        if therapy.is_active:
            active_therapies.append(therapy)

    compliance_data = []

    current_date = datetime.now().date()

    for therapy in active_therapies:
        total_expected = 0
        total_actual = 0
        missing_days = []

        for i in range(days):
            check_date = current_date - timedelta(days=i)

            # Expected intakes for this day
            expected_daily = therapy.daily_doses
            total_expected += expected_daily

            # Actual intakes for this day
            actual_daily = 0
            for mi in therapy.medication_intakes:
                if mi.intake_time.date() == check_date:
                    actual_daily += 1
            total_actual += actual_daily

            if actual_daily < expected_daily:
                missing_days.append(check_date)

        compliance_percentage = (total_actual / total_expected * 100) if total_expected > 0 else 0

        compliance_data.append({
            'therapy': therapy,
            'compliance_percentage': round(compliance_percentage, 1),
            'total_expected': total_expected,
            'total_actual': total_actual,
            'missing_days': missing_days,
            'status': 'good' if compliance_percentage >= 80 else 'poor' if compliance_percentage < 60 else 'moderate'
        })

    return compliance_data

@db_session
def check_glucose_thresholds_and_alert(patient_id):
    """Enhanced glucose alert system with different severity levels for doctors"""
    patient = Patient[patient_id]
    if not patient:
        return

    # Get recent glucose readings (last 24 hours)
    recent_readings = []
    cutoff_time = datetime.now() - timedelta(hours=24)
    for reading in patient.glucose_readings:
        if reading.measurement_time >= cutoff_time:
            recent_readings.append(reading)

    critical_readings = []
    high_readings = []

    for reading in recent_readings:
        # Critical thresholds (immediate attention)
        if (reading.is_before_meal and (reading.value < 60 or reading.value > 200)) or \
           (not reading.is_before_meal and reading.value > 300):
            critical_readings.append(reading)

        # High concern thresholds
        elif (reading.is_before_meal and (reading.value < 70 or reading.value > 160)) or \
             (not reading.is_before_meal and reading.value > 220):
            high_readings.append(reading)

    # Create alerts for doctor with different severity
    if critical_readings and patient.assigned_doctor:
        for reading in critical_readings:
            meal_status = "before meal" if reading.is_before_meal else "after meal"
            create_alert(
                patient_id,
                'glucose_critical',
                f"CRITICAL: Patient {patient.user.username} glucose {reading.value} mg/dL {meal_status} at {reading.measurement_time.strftime('%H:%M')}",
                'high',
                patient.assigned_doctor.id
            )

    if high_readings and patient.assigned_doctor:
        # Summarize high readings in one alert to avoid spam
        reading_summary = ", ".join([f"{r.value} mg/dL" for r in high_readings])
        create_alert(
            patient_id,
            'glucose_elevated',
            f"Patient {patient.user.username} has elevated glucose readings in last 24h: {reading_summary}",
            'medium',
            patient.assigned_doctor.id
        )

@db_session
def clear_compliance_alerts_for_patient(patient_id):
    """
    Rimuove tutti gli alert di compliance per un paziente quando riprende
    l'aderenza alla terapia
    """
    try:
        patient = Patient[patient_id]
        if not patient:
            return False

        # Find all unresolved compliance alerts for this patient
        compliance_alerts = []
        for alert in Alert.select():
            if (alert.patient == patient and
                alert.alert_type in ['compliance_issue', 'medication_missed'] and
                alert.resolved_at is None):
                compliance_alerts.append(alert)

        # Risolvi tutti gli alert di compliance
        for alert in compliance_alerts:
            alert.resolved_at = datetime.now()
            alert.is_read = True
        
        print(f"Cleared {len(compliance_alerts)} compliance alerts for patient {patient.user.username}")
        return True

    except Exception as e:
        print(f" Error clearing compliance alerts: {e}")
        return False

@db_session
def check_and_clear_compliance_alerts(patient_id):
    """
    Controlla se il paziente ha ripreso l'aderenza e rimuove gli alert se necessario.
    Viene chiamata dopo ogni registrazione di farmaco.
    """
    try:
        patient = Patient[patient_id]
        if not patient:
            return False

        # Check if patient is now compliant (has taken medications in last 2 days)
        recent_intakes = 0
        cutoff_time = datetime.now() - timedelta(days=2)
        for mi in MedicationIntake.select():
            if (mi.therapy.patient == patient and
                mi.intake_time >= cutoff_time):
                recent_intakes += 1

        # Se ha preso farmaci di recente, rimuovi gli alert di compliance
        if recent_intakes > 0:
            return clear_compliance_alerts_for_patient(patient_id)

        return False

    except Exception as e:
        print(f"Error checking compliance for alert cleanup: {e}")
        return False

@db_session
def clear_all_compliance_alerts():
    """
    Clear all existing compliance-related alerts before running new compliance checks.
    This prevents exponential accumulation of duplicate alerts.
    """
    try:
        # Define compliance-related alert types
        compliance_alert_types = [
            'medication_compliance',
            'patient_non_compliance', 
            'medication_reminder',
            'compliance_issue',
            'medication_missed'
        ]
        
        # Get all alerts and filter manually to avoid complex Pony ORM queries
        # Use a fresh query each time to avoid transaction conflicts
        cleared_count = 0
        
        # Process alerts in small batches to avoid long-running transactions
        batch_size = 10
        while True:
            batch_cleared = 0
            
            # Get a fresh batch of unresolved compliance alerts
            try:
                alerts_batch = []
                for alert in Alert.select():
                    if (alert.resolved_at is None and 
                        alert.alert_type in compliance_alert_types):
                        alerts_batch.append(alert)
                        if len(alerts_batch) >= batch_size:
                            break
                
                if not alerts_batch:
                    break  # No more alerts to process
                
                # Update this batch
                for alert in alerts_batch:
                    try:
                        # Check if alert is still unresolved (avoid race conditions)
                        if alert.resolved_at is None:
                            alert.resolved_at = datetime.now()
                            alert.is_read = True
                            batch_cleared += 1
                    except Exception:
                        # Skip this alert if there's a transaction conflict
                        continue
                
                cleared_count += batch_cleared
                
                # If we processed less than batch_size, we're done
                if len(alerts_batch) < batch_size:
                    break
                    
            except Exception as e:
                # If there's any transaction error, just break and report what we cleared
                print(f"Transaction conflict during alert clearing: {e}")
                break
        
        if cleared_count > 0:
            print(f"Cleared {cleared_count} existing compliance alerts before generating new ones")
        return cleared_count
        
    except Exception as e:
        print(f"Error clearing all compliance alerts: {e}")
        return 0

'''
    Questo file (operations.py) contiene tutte le operazioni del database per il sistema.
    Include funzioni per gestire utenti, pazienti, dottori, letture della glicemia,
    terapie, aderenza ai farmaci e sistema di allerte mediche.
'''