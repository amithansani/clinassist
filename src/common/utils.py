
import hashlib
from src.schemas.data_schema import PatientSchema, CredentialSchema, SymptomsSchema, MessagesSchema
from src.common.db_utils import DatabaseExecutions
from pandas import DataFrame
from src.common.logger import logging
from src.common.exception import CustomException
import re
import sys
import datetime

# Function to encrypt your password
def hashing(pwd):
    hash_object = hashlib.md5(bytes(str(pwd), encoding='utf-8'))
    hex_dig = hash_object.hexdigest()
    return hex_dig

def submit_registration(**patient_info):
    try:
        db = DatabaseExecutions(r"D:\Projects\LLM\clinassist\database\clinical_diagnosis.db")
        # Insert to Patient Table
        pat = PatientSchema(
            pat_id=None,
            pat_first_name=patient_info["pat_first_name"],
            pat_last_name=patient_info["pat_last_name"],
            email=patient_info["email"],
            gender=patient_info["gender"],
            date_of_birth=patient_info["date_of_birth"],
            address=patient_info["address"],
            city=patient_info["city"],
            state=patient_info["state"],
            country=patient_info["country"],
            contact_number=patient_info["contact_number"],
            pincode=patient_info["pincode"],
            smoking_status=patient_info["smoking_status"],
            alcohol_intake=patient_info["alcohol_intake"],
            exercise_frequency=patient_info["exercise_frequency"],
            dietary_preferences=patient_info["dietary_preferences"],
            dietary_restrictions=patient_info["dietary_restrictions"]
        )
        db.insert_data("patient", pat)
        cred = CredentialSchema(
            email=patient_info["email"],
            password=hashing(patient_info["password"])
        )
        db.insert_data("credential", cred)
        return True
    except Exception as e:
        return False

def check_password(email: str, password: str) -> bool:
    db = DatabaseExecutions(r"D:\Projects\LLM\clinassist\database\clinical_diagnosis.db")
    query = f"select password from credential where email = '{email}'"
    pass_df = db.execute_query(query)
    pass_db = pass_df.iloc[0][0]
    if pass_db == password:
        return True
    else:
        return False

def add_message(message: MessagesSchema) -> bool:
    try:
        db = DatabaseExecutions(r"D:\Projects\LLM\clinassist\database\clinical_diagnosis.db")
        db.insert_data("messages", message)
        return True
    except Exception as e:
        CustomException(e, sys)
        return False

def get_messages(chat_id: str) -> DataFrame:
    try:
        db = DatabaseExecutions(r"D:\Projects\LLM\clinassist\database\clinical_diagnosis.db")
        query = f"select * from messages where chat_id = '{chat_id}'"
        return db.execute_query(query)
    except Exception as e:
        return None

def get_symptoms(chat_id: str) -> DataFrame:
    db = DatabaseExecutions(r"D:\Projects\LLM\clinassist\database\clinical_diagnosis.db")
    query = f"select * from symptoms where chat_id = '{chat_id}'"
    symptoms = db.execute_query(query).to_dict(orient='list')
    return symptoms

def duration_to_days(duration_str) -> int:
    # Use regular expression to match the quantity and unit
    if duration_str == 'unknown':
        return 0
    match = re.match(r'\d+\s*\w+', duration_str)
    if not match:
        raise ValueError(f"Invalid duration format: {duration_str}")
    quantity = int(match.group().split()[0])
    unit = match.group().split()[1].rstrip('s')  # Remove plural form if any
    duration_mapping = {
        'day': 1,
        'week': 7,
        'month': 30,  # Approximate as month can have 28, 29, 30 or 31 days
        'year': 365  # Approximate as a year can have 365 or 366 days
    }
    if unit in duration_mapping:
        return quantity * duration_mapping[unit]
    else:
        raise ValueError(f"Unknown duration unit: {unit}")

def add_symptoms(symptoms_list: list, chat_id: str) -> bool:
    try:
        db = DatabaseExecutions(r"D:\Projects\LLM\clinassist\database\clinical_diagnosis.db")
        for symptom in symptoms_list:
            sym = SymptomsSchema(chat_id=chat_id, symptom_name=symptom["name"], duration=symptom["duration"])
            db.insert_data(table_name="symptoms", schema_instance=sym)
            logging.info(f"{symptom['name']} added to Symptom table")
        return True
    except Exception as e:
        CustomException(e, sys)
        return False

def get_last_ai_message(chat_id: str) -> str:
    db = DatabaseExecutions(r"D:\Projects\LLM\clinassist\database\clinical_diagnosis.db")
    query = f"select message from messages m where chat_id = '{chat_id}' and role = 'assistant' order by line_number desc Limit 1"
    last_message = db.execute_query(query)["message"].to_list()
    return last_message

def get_patient(email: str) -> str:
    db = DatabaseExecutions(r"D:\Projects\LLM\clinassist\database\clinical_diagnosis.db")
    query = f"select pat_first_name, pat_last_name, pat_id from patient where email = '{email}'"
    patient_df = db.execute_query(query)
    pat = patient_df.iloc[0][0]
    return pat
