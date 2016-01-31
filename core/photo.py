class Photo(object):
    """Represents a photo. Accepts a photo json object."""
    def __init__(self, ph):
        self.file_id = ph.get('file_id')
        self.file_size = ph.get('file_size')
        self.width = ph.get('width')
        self.height = ph.get('height')
