
import streamlit as st
from src.pages.chatbot import chat_window

def consultation_page():
    st.header("AI Clinical Assistant")
    st.subheader(f"Welcome {st.session_state.patient}")
    st.markdown('[Start Consultation](?page=chat_window)', unsafe_allow_html=True)
