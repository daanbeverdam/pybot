from send import Send


class SendMessage(Send):
    """Represents a message that will be sent by the bot."""
    def __init__(self):
        Send.__init__(self)
        self.text = None
        self.disable_web_page_preview = False  # (optional)
        self.parse_mode = 'Markdown'  # or 'HTML' (optional)
