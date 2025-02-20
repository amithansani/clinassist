
import streamlit as st
from src.common.utils import hashing, submit_registration

def registration_page():
    st.title("Register for ChatBot")
    st.subheader("Create a new account")

    # Define the tabs
    tabs = ["Login Info", "Demographics", "Medical History", "Lifestyle", "Family History"]
    # Use Streamlit's built-in tab functionality
    tab1, tab2, tab3, tab4, tab5 = st.tabs(tabs)

    # Login Info Tab
    with tab1:
        st.header("Login Info")
        email = st.text_input("Email", placeholder="Enter your email address",key="register_email")
        password = st.text_input("Password", placeholder="Enter your password", type="password",key="register_password")
        confirm_password = st.text_input("Confirm Password", placeholder="Enter your password", type="password")

    # Demographics Tab
    with tab2:
        st.header("Demographics")
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        date_of_birth = st.date_input("Date of Birth")
        address = st.text_area("Address", key="address")
        city = st.text_input("City")
        state = st.text_input("State")
        country = st.text_input("Country")
        pincode = st.text_input("Pincode")
        contact = st.text_input("Contact Number")

    # Medical History Tab
    with tab3:
        st.header("Medical History")
        medical_conditions = st.text_area("Medical Conditions")
        allergies = st.text_area("Allergies")
        medications = st.text_area("Current Medications")
        surgeries = st.text_area("Past Surgeries")

    # Lifestyle Tab
    with tab4:
        st.header("Lifestyle")
        alcohol_intake = st.selectbox("Alcohol Intake", ["None", "Occasional", "Regular"])
        exercise_frequency = st.selectbox("Exercise Frequency", ["None", "Occasional", "Regular", "Frequent"])
        diet = st.selectbox("Diet", ["Vegetarian", "Non-Vegetarian", "Other"])
        if diet == "Other":
            diet = st.text_input("Other")
        dietary_restrictions = st.text_input("Enter any Dietary Restrictions")

    # Family History Tab
    with tab5:
        st.header("Family History")
        family_genetic_diseases = st.text_input("Genetic Diseases in Family")

    # Example of a submit button
    if st.button("Submit"):
        patient_info = {
            "pat_first_name": first_name,
            "pat_last_name": last_name,
            "password": hashing(password),
            "email": email,
            "gender": gender,
            "date_of_birth": date_of_birth,
            "address": address,
            "city": city,
            "state": state,
            "country": country,
            "contact_number": contact,
            "pincode": pincode,
            "alcohol_intake": alcohol_intake,
            "exercise_frequency": exercise_frequency,
            "dietary_preferences": diet,
            "dietary_restrictions": dietary_restrictions
        }
        if submit_registration(**patient_info):
            st.write("Registration is successful")
        else:
            st.write("Unsuccessful")

registration_page()
