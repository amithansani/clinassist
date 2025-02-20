
import streamlit as st
from src.common.utils import check_password, hashing, get_patient
from src.common.logger import logging
from temp import session_state

def Login_page():
    st.title("Welcome to Our ChatBot Platform")
    st.subheader("Login to your account")
    container = st.container()
    with container:
        st.markdown("<div class='Login-box' id='Login'>", unsafe_allow_html=True)
        email = st.text_input("Email", placeholder="Enter your Registered Email")
        password = st.text_input("Password", placeholder="Enter your password", type="password")
        login_button = st.button("Login")
        if login_button:
            if check_password(email=email, password=hashing(password)):
                logging.info("Login Successful")
                st.write("Login Successful")
                st.session_state["email"] = email
                patient = get_patient(email=email)
                st.session_state["patient"] = patient
                st.session_state["logged_in"] = True
                session_state["patient"] = patient
            else:
                st.write("Login Unsuccessful")
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown('[Register here](?page=registration)', unsafe_allow_html=True)
