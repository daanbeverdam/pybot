from base_message import BaseMessage
from user import User
from chat import Chat


class Message(BaseMessage):
    """Represents a Telegram message. Extension of BaseMessage."""
    def __init__(self, message):
        BaseMessage.__init__(self, message)
        self.reply_to_message = BaseMessage(message.get('reply_to_message'))
