class Chat(object):
    """Represents a Telegram chat. Accepts a chat json object."""
    def __init__(self, ch):
        self.id = ch.get('id')
        self.type = ch.get('type')
        self.title = ch.get('title')
        self.first_name = ch.get('first_name')
        self.last_name = ch.get('last_name')
        self.username = ch.get('username')
