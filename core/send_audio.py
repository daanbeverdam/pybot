from send import Send


class SendAudio(Send):
    """Represents an audio file that will be sent by the bot."""
    def __init__(self, chat_id=None):
        Send.__init__(self, chat_id)
        self.audio = None  # file_id or string representation of audio file
        self.duration = None
        self.performer = None
        self.title = None
