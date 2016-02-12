from send import Send


class ForwardMessage(Send):
    """Represents a message that will be forwarded."""
    def __init__(self, chat_id=None):
        Send.__init__(self, chat_id)
        self.from_chat_id = None
        self.message_id = None
