class Message():

    def __init__(self, message):
        self.id = message.get('message_id')
        self.date = message.get('date')
        self.text = message.get('text')
        self.sender = message.get('from')
        self.first_name_sender = self.sender['first_name']
        self.chat = message['chat']
        self.chat_id = self.chat['id']
        self.contains_command = self.check_for_command()

    def check_for_command(self):
        if self.text.startswith('/'):
            return True
        else:
            return False