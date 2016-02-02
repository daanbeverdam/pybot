import shelve
import traceback
import StringIO
import urllib
from response import Response


class Command(object):

    def __init__(self, name, dialogs={}, requires_arguments=False, admin_id=0,
                 api_key=0, is_always_listening=False, language='en'):
        self.name = name
        self.dialogs = dialogs
        self.usage = dialogs.get('usage')
        self.message = None
        self.data = None
        self.arguments = None
        self.requires_arguments = requires_arguments
        self.admin = int(admin_id)  # TODO: make user?
        self.api_key = api_key
        self.is_waiting_for_input = False
        self.has_scheduled_event = False
        self.is_always_listening = is_always_listening
        self.default_language = language
        self.response = Response()

    def listen(self, message):
        self.message = message
        self.arguments = self.get_arguments()
        self.data = shelve.open('data/chat_' + str(message.chat.id))
        self.collect_user_data(message)

        tokens = message.text.split()
        if tokens[0] == self.name:
            # if len(tokens) > 1 and tokens[1] == 'help':
            #     self.response.text = self.usage
            #     return self.response
            # if len(tokens) == 1 and self.accepts_none_argument is False:
            #     return 'ask for input'
            return True
        elif '@' in message.text and self.message.text.split('@')[0] == self.name:
            return True
        elif self.is_active() or self.is_always_listening:
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
