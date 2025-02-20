
import sys
from langgraph.graph import END, StateGraph, START
from typing import List, Optional, Dict, Union
from pydantic import BaseModel
from langchain_core.messages import MessageLikeRepresentation
from src.agents.message_validator_agent import MessageValidator
from src.common.utils import add_symptoms, get_symptoms, get_last_ai_message, duration_to_days
from src.common.exception import CustomException
from src.common.logger import logging
from src.agents.symptom_checker_responder import SymptomCheckerResponder
from src.agents.response_generator_agent import ResponseGenerator

Messages = Union[List[MessageLikeRepresentation], MessageLikeRepresentation]

class SymptomBaseModel(BaseModel):
    name: str
    duration: Optional[int]

class ConversationState(BaseModel):
    chat_id: str=""
    symptoms: List[SymptomBaseModel] = []
    medical_history: List[str] = []
    message_history: str = None
    last_message: MessageLikeRepresentation = None
    message_valid: str = None
    message_response: str = "No response"
    final_message: bool = False

def validate_message(state: ConversationState) -> ConversationState:
    logging.info("Message Validation Started")
    last_message = state.last_message
    message_history = state.message_history
    message_valid = MessageValidator(last_message, message_history).response
    state.message_valid = "ERROR" if message_valid not in ["True", "False"] else message_valid
    return state

def check_message_validity(state: ConversationState) -> bool:
    valid = state.message_valid
    if valid == "True":
        return True
    elif valid == "False":
        return False
    raise Exception

def ask_user(state: ConversationState) -> ConversationState:
    state.message_response = ResponseGenerator(input_text=state.last_message, message_history=state.message_history, response_type="invalid message").response
    return state

def symptom_detector(state: ConversationState) -> ConversationState:
    response = SymptomCheckerResponder(state.last_message, state.message_history).response

    state.message_response = response["message_response"]

    symptoms = []
    for symptom in response["symptoms"]:
        try:
            duration_days=duration_to_days(str(symptom["duration"]))
            sym = SymptomBaseModel(name=symptom["symptom_name"], duration=duration_to_days(str(symptom["duration"])))
        except Exception as e:
            print(e)
        symptoms.append(sym)
    state.symptoms = symptoms
    state.final_message = response.get("final_message", False)
    return state

def is_final_message(state: ConversationState) -> bool:
    return state.final_message

def save_symptoms(state: ConversationState) -> ConversationState:
    symptoms = state.symptoms
    add_symptoms(symptoms, state.chat_id)
    return state

def create_graph():
    # checkpoint = MemorySaver()


    try:
        workflow = StateGraph(ConversationState)
        logging.info("Workflow Started")
        workflow.add_node("validate_message", validate_message)
        workflow.add_node("symptom_detector", symptom_detector)
        workflow.add_node("ask_user", ask_user)
        workflow.add_node("save_symptoms", save_symptoms)
        workflow.add_edge(START, "validate_message")
        workflow.add_conditional_edges("validate_message", check_message_validity,
                                       {True: "symptom_detector", False: "ask_user"})
        workflow.add_conditional_edges("symptom_detector", is_final_message, {True: "save_symptoms", False: END})
        return workflow.compile()


    except Exception as e:

        CustomException(e, sys)

# from graphviz import Digraph

# def render_graph(graph):
#     dot = Digraph(comment='langGraph Workflow')
#     for node in graph.nodes:
#         dot.node(node)
#     for edge in graph.edges:
#         dot.edge(*edge)
#     return dot

if __name__ == "__main__":
    s = ConversationState(last_message="I have headache since 2 days", chat_id="345")
    app = create_graph()
    fs = app.invoke(s)
    print(fs)
