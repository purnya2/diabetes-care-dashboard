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
    email = Optional(str)
    is_active = Required(bool, default=True)
    is_admin = Required(bool, default=False)
    managed_projects = Set('Project', cascade_delete=True, reverse="manager")
    member_of_projects = Set('Project', reverse="members")

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.id)

class Patient(User):
    doctor = Optional('Doctor', reverse='patients')
    measurements = Set('Measurement', reverse='patient')
    symptoms = Set('Symptom', reverse='patient')
    medications = Set('Medication', reverse='patient')
    therapies = Set('Therapy', reverse='patient')

class Doctor(User):
    patients = Set('Patient', reverse='doctor')
    therapies = Set('Therapy', reverse='doctor')


class Measurement(db.Entity):
    patient = Required('Patient', reverse='measurements')
    timestamp = Required(datetime)
    value = Required(float)  # mg/dL
    before_meal = Required(bool)  # True if before meal, False if after

class Symptom(db.Entity):
    patient = Required('Patient', reverse='symptoms')
    name = Required(str)
    description = Optional(str)
    start_date = Required(datetime)
    end_date = Optional(datetime)


class Medication(db.Entity):
    name = Required(str)
    type = Required(str)  # e.g., insulin, oral antidiabetic
    dose = Required(float)
    unit = Required(str)  # e.g., mg, IU
    intake_time = Required(datetime)
    therapy = Optional('Therapy', reverse='medications')
    patient = Optional('Patient', reverse='medications')

class Therapy(db.Entity):
    patient = Optional('Patient', reverse='therapies')
    doctor = Required('Doctor', reverse='therapies')
    drug_name = Required(str)
    daily_intakes = Required(int)
    dose_per_intake = Required(float)
    unit = Required(str)
    instructions = Optional(str)
    start_date = Required(datetime)
    end_date = Optional(datetime)
    medications = Set('Medication', reverse='therapy')