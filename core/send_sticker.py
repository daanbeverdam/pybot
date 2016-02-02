from send import Send


class SendSticker(Send):
    """Represents a sticker that will be sent by the bot."""
    def __init__(self):
        self.sticker = None  # file_id or string representation of sticker
