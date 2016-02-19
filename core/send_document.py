from send import Send


class SendDocument(Send):
    """Represents a document that will be sent by the bot."""

    def __init__(self, chat_id=None):
        Send.__init__(self, chat_id)
        self.document = None  # file_id or string representation of file
        self.name = None
