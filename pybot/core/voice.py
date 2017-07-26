class Voice(object):
    """Represents a voice message. Accepts a voice json object."""
    def __init__(self, vo):
        self.duration = vo.get('duration')
        self.mime_type = vo.get('mime_type')
        self.file_id = vo.get('file_id')
        self.file_size = vo.get('file_size')
