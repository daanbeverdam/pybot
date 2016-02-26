from thumb import Thumb


class Document(object):
    """Represents a sent document."""
    def __init__(self, do):
        self.file_name = do.get('file_name')
        self.mime_type = do.get('mime_type')
        if do.get('thumb'):
            self.thumb = Thumb(do.get('thumb'))
        self.file_id = do.get('file_id')
        self.file_size = do.get('file_size')
