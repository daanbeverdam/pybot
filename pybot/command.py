class Command(object):

    def __init__(self, name, dialogs):
        self.name = name
        self.dialogs = dialogs
        self.usage = dialogs['usage']
        self.reply_text = dialogs['reply']
        self.message = None

    def listen(self, message):
        if message.text.startswith('/') and message.text.split(' ', 1)[0][1:] == self.name:
            self.message = message
            return True
        return False

    def arguments(self):
        if len(self.message.text.split(' ')) > 1:
            return self.message.text.split(' ', 1)[1]
