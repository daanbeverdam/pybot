class Message(object):
    def __init__(self, message):
        self.id = message['message_id']
        self.chat = message['chat']
        self.text = message['text']
        self.sender = message['from']

        self.command = self.get_command()

    def get_command(self):
        tokens = self.text.split(' ')

        if tokens[0].startswith('/') and tokens[0][1:] in Command.commands:
            return Command.commands[tokens[0][1:]]

        return None
