
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate, ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.prompts import FewShotChatMessagePromptTemplate, PromptTemplate
from langchain import PromptTemplate
from src.common.llm_model import GroqModel
from langchain.memory import ConversationBufferMemory
from src.common.logger import logging
from src.common.exception import CustomException
import sys
import ast
import json

class SymptomCheckerResponder:
    def __init__(self, input_text: str, message_history: str):
        try:

            self.input_text = input_text
            self.message_history = message_history
            self.llm = GroqModel
            # self.memory = ConversationBufferMemory
            self.prompt = self._define_prompt()
            self.chain = self._define_chain()
            self.response = self._generate_response()
        except Exception as e:
            print(e)

    def _define_prompt(self) -> ChatPromptTemplate:
        system = f"""
        You are an AI Assistant for analyzing symptoms for patients from chat messages.
        User may tell about symptoms. 
        Follow the below steps:
        1. Check if we have duration provided in the symptoms.
        2. If you have the duration of all the symptoms provided by the user, ask the user if any other problems are faced.
        3. If any other symptoms mentioned, expand it in the previous symptoms. Append all the symptoms detected in the historical messages in the Symptom list.
        4. If user says no other issues, you need to format the response, no further follow up is required with the user.
        5. Your each response should Look Like Dict(Message_response="<generated message>", Symptoms = [Dict(symptom_name=<name of symptom>, duration=<duration in days>)]).
        6. Any durations which is not in days like yesterday, today etc. Convert it to days. Example convert yesterday to 1 day, today as 0 days.
        7. Don't return duration in any other format other than in days/hours/months/years. Make sure to add the unit as shown in example
        8. Just now means duration = 0 days.
        9. If duration is in range like 2-3 days take it as higher day i.e. 3 days.
        10. In message response don't extend any other question. Just stick to getting duration and symptoms. If user talks about any other thing, don't consider it.
        11. You should not send any treatment recommendations. You task is just to analyze and collect all relevant information.
        Few Examples of the conversations for you to understand:
        Example 1:
        AI Assistant: Please provide your symptoms and duration.
        Human: I have headache.
        AI Assistant: Since when you are facing headache?
        Human: 3 days.
        Your response should Look Like:
        1st response: Dict("message_response": "Since when you are facing headache", "symptoms": [Dict("symptom_name": "headache", "duration": "unknown")], "final_message": "false").
        2nd response: Dict("message_response": "Are you having any other health issues?", "symptoms": [Dict("symptom_name": "headache", "duration": "3 days")], "final_message": "false").
        3rd response: Dict("message_response": "Thanks for providing me the information. Allow me to process the information provided.", "symptoms": [Dict("symptom_name": "headache", "duration": "3 days")], "final_message": "true").
        Note that how all the symptoms are added in the Symptoms key in the Last message. It is used from the previous messages.
        Don't add any other field.
        No other explanation is required.
        Use History
        message history:{self.message_history}
        Dict is a dictionary format. Dont show keyword Dict instead show curly braces. Keys in dict should always in lower case
        """
        human = "{text}"
        prompt = ChatPromptTemplate.from_messages([("system",system),("human", human)])
        return prompt

    def _define_chain(self) -> LLMChain:
        try:
            print("defining Chain")
            return self.prompt | self.llm
        except Exception as e:
            print(e)


    def _generate_response(self) -> str:
        try:
            print("generating response")
            response = self.chain.invoke({"text": self.input_text})
            logging.info("Symptoms detected")
            logging.info(f"LLM Response: {response}")
            # response_dict = ast.literal_eval(response.content)
            response_dict = json.loads(response.content)
            logging.info(f"Response converted to dict: {response_dict}")
        except Exception as e:
            CustomException(e, sys)
            response_dict = {"error": str(e)}
        logging.info(f"Symptom Detector Agent Result: {response_dict}")
        return response_dict
