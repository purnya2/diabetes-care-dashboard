from datetime import datetime
from typing import List, Optional

class GlycemiaMeasurement:
  def __init__(self, date: datetime, pre_meal: Optional[float] = None, post_meal: Optional[float] = None):
    self.date = date
    self.pre_meal = pre_meal  # mg/dL
    self.post_meal = post_meal  # mg/dL

class Symptom:
  def __init__(self, name: str, start_date: datetime, end_date: Optional[datetime] = None):
    self.name = name
    self.start_date = start_date
    self.end_date = end_date

class MedicationIntake:
  def __init__(self, date: datetime, time: str, medication: str, quantity: float):
    self.date = date
    self.time = time
    self.medication = medication
    self.quantity = quantity

class TherapyOrPathology:
  def __init__(self, name: str, start_date: datetime, end_date: Optional[datetime] = None):
    self.name = name
    self.start_date = start_date
    self.end_date = end_date

class User:
  def __init__(self, user_id: int, name: str, role: str):
    self.user_id = user_id
    self.name = name
    self.role = role  # 'diabetologist' or 'patient'
    self.glycemia_measurements: List[GlycemiaMeasurement] = []
    self.symptoms: List[Symptom] = []
    self.medication_intakes: List[MedicationIntake] = []
    self.therapies_or_pathologies: List[TherapyOrPathology] = []

  def add_glycemia_measurement(self, measurement: GlycemiaMeasurement):
    self.glycemia_measurements.append(measurement)

  def add_symptom(self, symptom: Symptom):
    self.symptoms.append(symptom)

  def add_medication_intake(self, intake: MedicationIntake):
    self.medication_intakes.append(intake)

  def add_therapy_or_pathology(self, therapy_or_pathology: TherapyOrPathology):
    self.therapies_or_pathologies.append(therapy_or_pathology)