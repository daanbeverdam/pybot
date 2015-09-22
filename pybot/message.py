class Message(object):

    def __init__(self, message):
        self.id = message.get('message_id')
        self.date = message.get('date')
        self.text = message.get('text')
        self.sender = message.get('from')
        self.first_name_sender = self.sender['first_name']
        self.sender_id = self.sender['id']
        self.chat = message['chat']
        self.chat_id = self.chat['id']
        self.contains_command = self.check_for_command()

    def check_for_command(self):
        if (self.text is not None and self.text.startswith('/') and
                len(self.text) > 1):
            return True
        return False
