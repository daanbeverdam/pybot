from send import Send


class SendPhoto(Send):
    """Represents a photo that will be sent."""
    def __init__(self, chat_id=None):
        Send.__init__(self, chat_id)
        self.photo = None  # file_id or string representation of image
        self.name = None  # including file extension (i.e.: .jpg)
        self.caption = None
