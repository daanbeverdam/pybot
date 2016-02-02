class SendPhoto(object):
    """Represents a photo that will be sent."""
    def __init__(self):
        self.photo = None  # file_id or string representation of image
        self.caption = None
