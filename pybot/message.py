import pybot
from command import Command

class Message(object):
    
    def __init__(self, message):
        self.id = message.get('message_id')
        self.date = message.get('date')
        self.text = message.get('text')
        self.sender = message.get('from')
        self.first_name_sender = self.sender['first_name']
        self.chat = message['chat']
        self.chat_id = self.chat['id']
        self.command = self.get_command()

    def get_command(self):
        tokens = self.text.split(' ')
        if tokens[0].startswith('/') and tokens[0][1:] in PyBot.commands:
            return Command(tokens[0][1:], tokens[1:])
        else:
            return None
