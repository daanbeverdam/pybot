import shelve
import traceback
import StringIO
import urllib
from response import Response
from user import User


class Command(object):

    def __init__(self, name, dialogs={}, requires_arguments=False, admin_id=0,
                 api_key=0, is_always_listening=False, language='en'):
        self.name = name  # command name including slash /
        self.dialogs = dialogs
        self.usage = dialogs.get('usage')
        self.message = None
        self.data = None
        self.arguments = None
        self.requires_arguments = requires_arguments
        self.admin = int(admin_id)  # TODO: make user?
        self.api_key = api_key  # optional; only if the command needs it
        self.is_waiting_for_input = False
        self.is_waiting_for = User()
        self.has_scheduled_event = False
        self.is_always_listening = is_always_listening
        self.is_waiting_for_input = False
        self.default_language = language

    def listen(self, message):
        self.message = message
        self.response = Response(self.message.chat.id)
        self.arguments = self.get_arguments()
        self.data = shelve.open('data/chat_' + str(message.chat.id))
        self.collect_user_data(message)

        tokens = message.text.split()
        if tokens[0].lower().split('@')[0] == self.name:
            return True
        elif self.is_active() or self.is_always_listening or self.is_waiting_for_input:
            return True
        return False

    def is_active(self):
        try:
            if self.data[self.name + '_active']:
                return True
        except:
            self.data[self.name + '_active'] = False
        return False

    def activate(self, boolean=True):
        if boolean is False:
            self.data[self.name + '_active'] = False
        else:
            self.data[self.name + '_active'] = True

    def collect_user_data(self, message):
        try:
            if str(message.sender.id) not in self.data['chat_users']:
                temp_dict = self.data['chat_users']
                temp_dict[str(message.sender.id)] = message.sender
                self.data['chat_users'] = temp_dict
        except:
            self.data['chat_users'] = {}

    def get_arguments(self):
        if len(self.message.text.split()) > 1:
            return self.message.text.split(' ', 1)[1]

    def get_image(self, image_link):
        return StringIO.StringIO(urllib.urlopen(image_link).read()).getvalue()
