class User(object):
    """Represents a Telegram User. Accepts 'from' json object."""
    def __init__(self, fr):
        self.id = fr.get('id')
        self.first_name = fr.get('first_name')
        self.last_name = fr.get('last_name')
        self.username = fr.get('username')
