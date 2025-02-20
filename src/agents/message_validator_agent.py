
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate, ChatPromptTemplate
from langchain.chains import LLMChain
from src.common.llm_model import GroqModel
from langchain.memory import ConversationBufferMemory
from src.common.logger import logging
from src.common.exception import CustomException
import sys

class MessageValidator:
    def __init__(self, input_text: str, message_history: str):
        self.input_text = input_text
        self.message_history = message_history
        self.llm = GroqModel
        self.memory = ConversationBufferMemory()
        self.prompt = self._define_prompt()
        self.chain = self._define_chain()
        self.response = self._validate_message()

    def _define_prompt(self) -> ChatPromptTemplate:
        system = (
            """You are AI assistant for analyzing symptoms for patients from chat messages"""
            """Your task is to check if the user's chat messages could be asked to a chat assistant"""
            """Some questions may be follow-up for the doctor's agent so may not have symptoms, but may have answers to questions"""
            """You just need to classify if that is a relevant message or not"""
            """If message is just a Letter, set as irrelevant"""
            """If message is just a letter, set as irrelevant"""
            """Do not mark a message as TRue just be seeing if it has symptoms. You must check if it is correct as per the context"""
            """Check for metaphors.Like Coding is a headache.So it is irrelevant"""
            """Example:If the user says:I want to fly without having a headache, it is not relevant."""
            """Example: If the user says: When I got to know that he is fired I almost had a heart attack, it is not relevant."""
            """Answer in just True or False.Explanation is not required"""
        )
        human = "{text}"
        prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])
        return prompt

    def _define_chain(self) -> LLMChain:
        return self.prompt | self.llm

    def _validate_message(self) -> str:
        try:
            response = self.chain.invoke({"text": self.input_text})
            logging.info("Message Validation Completed")
            logging.info(f"Message Validation: Response from LLM - {response}")
            response = response.content
        except Exception as e:
            CustomException(e, sys)
            response = "error"
        logging.info(f"Message Validation Result: {response}")
        return response

# Example usage
if __name__ == "__main__":
    input_question = "3 days"
    message_validator = MessageValidator(input_question, "")
    input_question = "5 days"
