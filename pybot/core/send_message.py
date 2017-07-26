from pybot.core.send import Send


class SendMessage(Send):
    """Represents a message that will be sent by the bot."""

    def __init__(self, chat_id=None):
        Send.__init__(self, chat_id)
        self.text = None
        self.disable_web_page_preview = False  # (optional)
        self.parse_mode = None  # 'Markdown' or 'HTML' (optional)
