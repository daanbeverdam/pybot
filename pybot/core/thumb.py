class Thumb(object):
    """Represents a thumbnail of a sent file or sticker.
    Accepts thumb json object as input"""
    def __init__(self, thumb):
        self.file_id = thumb.get('file_id')
        self.file_size = thumb.get('file_size')
        self.width = thumb.get('width')
        self.height = thumb.get('height')
