
import streamlit as st
from src.pages.login import Login_page
from src.pages.registration import registration_page
from src.pages.home import home_page
from src.pages.chatbot import chat_window

def initialize_session_state():
    if "new_conv" not in st.session_state:
        st.session_state["new_conv"] = False
    if "patient" not in st.session_state:
        st.session_state["patient"] = None

def main():
    # Determine page from query parameters
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    query_params = st.query_params
    page = query_params.get("page", "Login")
    if st.session_state["logged_in"]:
        home_page()
    elif page == "registration":
        registration_page()
    elif page == "chat_window": 
        st.session_state["conv_status"] = "new"
        chat_window()
    else:
        initialize_session_state()
        Login_page()

if __name__ == "__main__":
    main()
