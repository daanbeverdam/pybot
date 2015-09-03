import shelve
import os


class Command(object):

    def __init__(self, name, dialogs):
        self.name = name
        self.dialogs = dialogs
        self.usage = dialogs['usage']
        self.message = None
        self.meta_commands = ['/done', '/cancel', '/results']
        self.data = None

    def listen(self, message):
        tokens = message.text.split(' ')
        self.message = message
        if message.text.startswith('/') and tokens[0][1:] == self.name:
            return True
        elif self.is_active():
            return True
        return False

    def is_active(self):
        self.data = shelve.open('data/chat_' + str(self.message.chat_id))
        try:
            if self.data[self.name + '_active']:
                return True
        except:
            self.data[self.name + '_active'] = False
        return False

    def arguments(self):
        if len(self.message.text.split(' ')) > 1:
            return self.message.text.split(' ', 1)[1]
