
from dataclasses import dataclass
from typing import Optional
import hashlib
from datetime import date, datetime

@dataclass
class PatientSchema:
    pat_id: Optional[int]
    pat_first_name: str
    pat_last_name: str
    email: str
    gender: str
    date_of_birth: str
    address: str
    city: str
    state: str
    country: str
    pincode: str
    contact_number: str
    smoking_status: str
    alcohol_intake: str
    exercise_frequency: str
    dietary_preferences: str
    dietary_restrictions: str

@dataclass
class CredentialSchema:
    email: str
    password: str

class PatientMedicalHistory:
    def __init__(self, pat_med_hist_id: Optional[int], pat_id: int, medical_history: str, date_since: date):
        self.pat_med_hist_id = pat_med_hist_id
        self.pat_id = pat_id
        self.medical_history = medical_history
        self.date_since = date_since

class PatientAllergies:
    def __init__(self, pat_allergy_id: Optional[int], pat_id: int, allergy: str, date_since: date):
        self.pat_allergy_id = pat_allergy_id
        self.pat_id = pat_id
        self.allergy = allergy
        self.date_since = date_since

class PatientCurrentMedications:
    def __init__(self, pat_curr_med_id: Optional[int], pat_id: int, medication: str, date_since: date):
        self.pat_curr_med_id = pat_curr_med_id
        self.pat_id = pat_id
        self.medication = medication
        self.date_since = date_since

class PatientPastSurgeries:
    def __init__(self, pat_past_surg_id: Optional[int], pat_id: int, past_surgery: str, date_since: date):
        self.pat_past_surg_id = pat_past_surg_id
        self.pat_id = pat_id
        self.past_surgery = past_surgery
        self.date_since = date_since

class FamilyChronicIllness:
    def __init__(self, chronic_illness_id: Optional[int], pat_id: int, chronic_illness: str, date_since: date):
        self.chronic_illness_id = chronic_illness_id
        self.pat_id = pat_id
        self.chronic_illness = chronic_illness
        self.date_since = date_since

class FamilyGeneticDisease:
    def __init__(self, genetic_disease_id: Optional[int], pat_id: int, genetic_disease: str, date_since: date):
        self.genetic_disease_id = genetic_disease_id
        self.pat_id = pat_id
        self.genetic_disease = genetic_disease
        self.date_since = date_since

@dataclass
class MessagesSchema:
    chat_id: str
    line_number: int
    pat_id: int
    message: str
    role: str
    message_dtm: datetime

@dataclass
class SymptomsSchema:
    chat_id: str
    symptom_name: str
    duration: int
    # severity: str
