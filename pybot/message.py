from command import Command

class Message():
    
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
        first_word = self.text.split(' ')[0]
        command_name = first_word[1:]
        arguments = self.text.split(' ',1)[1] if len(self.text.split(' ')) > 1 else None
        if first_word.startswith('/') and command_name in Command.dictionary:
            return Command(command_name, arguments)
        else:
            return None
