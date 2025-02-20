
from src.common.db_utils import DatabaseExecutions

db = DatabaseExecutions("database/clinical_diagnosis.db")

db.create_table(ddl_query = """
    CREATE TABLE credential (
        email TEXT PRIMARY KEY,
        password TEXT NOT NULL
    )
"""
                )

db.create_table(ddl_query = """
    CREATE TABLE messages (
        chat_id TEXT,
        line_number INTEGER,
        pat_id INTEGER,
        message TEXT NOT NULL,
        role TEXT NOT NULL,
        message_dtm DATETIME,
        final_message INTEGER,
        CONSTRAINT MESSAGES_PK PRIMARY KEY (chat_id, line_number)
    )
"""
                )



db.create_table(ddl_query = """
    CREATE TABLE patient (
        last_name TEXT,
        email TEXT NOT NULL UNIQUE,
        gender TEXT NOT NULL,
        date_of_birth DATE,
        contact_number TEXT NOT NULL,
        smoking_status TEXT NOT NULL,
        alcohol_intake TEXT NOT NULL,
        exercise_frequency TEXT NOT NULL,
        dietary_preferences TEXT NOT NULL,
        dietary_restrictions TEXT
    )
"""
                )

db.create_table(ddl_query = """
    CREATE TABLE symptoms (
        chat_id TEXT NOT NULL,
        symptom_name TEXT NOT NULL,
        duration INTEGER,
        CONSTRAINT SYMPTOMS_PK PRIMARY KEY (chat_id, symptom_name)
    )
"""
                )