class User(object):
    """Represents a Telegram User. Accepts 'from' json object."""
    def __init__(self, fr=None, id=None, first_name=None, last_name=None,
                 username=None, is_bot=None):
        if fr:  # allows for initialization without json
            self.id = fr.get('id')
            self.first_name = fr.get('first_name')
            self.last_name = fr.get('last_name')
            self.username = fr.get('username')
            self.is_bot = fr.get('is_bot')
        else:
            self.id = id
            self.first_name = first_name
            self.last_name = last_name
            self.username = username
            self.is_bot = is_bot

    def get_full_name(self):
        """Returns full first and second name (if provided)."""
        if self.first_name and self.last_name:
            return self.first_name + ' ' + self.last_name
        else:
            return self.first_name

