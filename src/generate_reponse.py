
from src.workflow import ConversationState, create_graph
from src.common.utils import get_messages
from src.common.logger import logging
from src.common.exception import CustomException
import sys

class MessageResponse:
    def __init__(self, last_message: str, chat_id: str):
        self.last_message = last_message
        self.chat_id = chat_id
        self.message_history = self._get_message_history()
        self.response = self._get_final_response()

    def _get_final_response(self):
        try:
            state = ConversationState()
            state.last_message = self.last_message
            state.message_history = self.message_history
            # state.message_history=["No history"]
            state.chat_id = self.chat_id
            logging.info("Workflow starting")
            app= create_graph()
            final_state=app.invoke(state)
            logging.info(f"Final state: {final_state}")
            response = final_state["message_response"]
            logging.info(final_state)
        except Exception as e:
            response = "Internal Server Error! Please retry with other message. Sorry for the inconvenience"
            CustomException(e, sys)
        finally:
            return response

    def _get_message_history(self):
        messages = get_messages(self.chat_id)
        return "\n".join(list(messages["role"] + " : " + messages["message"]))

if __name__ == "__main__":
    prompt = "I have headache since 2 days"
    response = MessageResponse(prompt, chat_id="123").response
    print(response)
