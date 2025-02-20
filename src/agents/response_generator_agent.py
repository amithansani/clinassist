
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate, ChatPromptTemplate
from langchain.chains import LLMChain
from src.common.llm_model import GroqModel
from langchain.memory import ConversationBufferMemory
from src.common.logger import logging
from src.common.exception import CustomException
import sys

class ResponseGenerator:
    def __init__(self, input_text: str, response_type: str, message_history: str = None, last_ai_message: str = None):
        self.input_text = input_text
        self.message_history = message_history
        self.response_type = response_type
        self.last_ai_message = last_ai_message
        self.llm = GroqModel
        self.memory = ConversationBufferMemory()
        self.prompt = self._define_prompt()
        self.chain = self._define_chain()
        self.response = self._validate_message()

    def _define_prompt(self) -> ChatPromptTemplate:
        if self.response_type == "invalid message":
            system = (
                """You are an AI assistant for anayysing symptoms for the patients from chat messages and respond"""
                """The user last message is invalid"""
                """Generate a response to the user after analysing the message history"""
                """Be polite to the user's message but make sure user understands that this is a clnical assistant tool and he should refrain from sending irrelevant messages"""
                f"""message history:{self.message_history}"""
                """Send response in string format only. No metadata required"""
            )
            prompt = ChatPromptTemplate.from_messages([("system", system), ("human", self.input_text)])
            return prompt
        elif self.response_type == "no symptoms":
            system = "You are an AI Assistant for analyzing symptoms for patients from chat messages and responding accordingly.\nPrepare a response if the message by the user is relevant.\nExample: Last AI Message: Since how long have you been facing back pain? User response: 3 days. It should be relevant.\nSend a response in string format only. No metadata required.\n\nLast AI Message: {}\nHuman: {}".format(self.last_ai_message, self.input_text)
            prompt = ChatPromptTemplate.from_messages([("system", system), ("human", self.input_text)])
            return prompt

    def _define_chain(self) -> LLMChain:
        return LLMChain(prompt=self.prompt, llm=self.llm, memory=self.memory)

    def _validate_message(self) -> str:
        try:
            response = self.chain.invoke({"text": self.input_text}).content
            return response
        except Exception as e:
            CustomException(e, sys)
            return "Internal Server Error! Please retry with another message. Sorry for the inconvenience."
