
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


GroqModel = ChatGroq(model="llama-3.3-70b-versatile")
# mixtra_l = ChatGroq(model="mixtra-l-8x7b-32768")
