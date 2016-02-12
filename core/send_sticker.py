from send import Send


class SendSticker(Send):
    """Represents a sticker that will be sent by the bot."""
    def __init__(self, chat_id=None):
        Send.__init__(self, chat_id)
        self.sticker = None  # file_id or string representation of sticker
