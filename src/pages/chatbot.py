
import streamlit as st
from src.generate_reponse import MessageResponse
from src.schemas.data_schema import MessagesSchema
from src.common.utils import add_message
from datetime import datetime
from uuid import uuid1
from src.common.logger import logging
from temp import session_state

def chat_window():
    st.title("AI Clinical Assistant")
    
    # setting chat_id
    if "chat_id" not in st.session_state:
        st.session_state.chat_id = str(uuid1())
        logging.info(f"Conversation Started. Chat ID: {st.session_state.chat_id}\n")
    st.subheader(f"Chat ID: {st.session_state.chat_id}")
    st.subheader("Use This Chat ID for further references")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": f"Hello {session_state['patient']}. Please tell me your symptoms and duration",
                "line_number": 1
            }
        ]
        
    # Add message to database
    msg = MessagesSchema(
        chat_id=st.session_state.chat_id, 
        line_number=1, 
        pat_id=None, 
        message='Hello. Please tell me your symptoms and duration', 
        role="assistant", 
        message_dtm=datetime.now()
    )
    add_message(msg)
    
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
    if prompt := st.chat_input("Type your message: "):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Add user message to chat history
        new_line_number = st.session_state.messages[-1]["line_number"] + 1
        
        # Add message to database
        msg = MessagesSchema(
            chat_id=st.session_state.chat_id, 
            line_number=new_line_number, 
            pat_id=None, 
            message=prompt, 
            role="user", 
            message_dtm=datetime.now()
        )
        if add_message(msg):
            logging.info("Message Added in Message Table")
        else:
            logging.info("Message not added in Message Table")
        
        # Get chatbot response
        logging.info("Getting Response")
        response = MessageResponse(prompt, chat_id=st.session_state.chat_id).response
        
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        
        # Add assistant response to chat history
        new_line_number = st.session_state.messages[-1]["line_number"] + 1
        st.session_state.messages.append({
            "role": "assistant",
            "content": response,
            "line_number": new_line_number
        })
        
        # Add message to database
        msg = MessagesSchema(
            chat_id=st.session_state.chat_id, 
            line_number=new_line_number, 
            pat_id=None, 
            message=response, 
            role="assistant", 
            message_dtm=datetime.now()
        )
        add_message(msg)
