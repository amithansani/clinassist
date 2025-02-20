
import streamlit as st
from src.pages.consultation import consultation_page
from src.pages.upload import upload_report_page
from src.pages.history import history_page

def home_page():
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", ["Create new consultation", "Upload report", "Open History"])
    if selection == "Create new consultation":
        consultation_page()
    elif selection == "Upload report":
        upload_report_page()
    elif selection == "Open History":
        history_page()
