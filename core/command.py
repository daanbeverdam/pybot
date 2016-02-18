import shelve
import traceback
from StringIO import StringIO
import urllib
from response import Response
from user import User


class Command(object):
    """Base class for commands."""

    def __init__(self, name, dialogs={}, requires_arguments=False, admin_id=0,
                 api_key=0, is_always_listening=False, language='en'):
        self.name = name  # command name including slash /
        self.dialogs = dialogs
        self.usage = dialogs.get('usage')
        self.message = None
        self.data = None
        self.arguments = None
        self.requires_arguments = requires_arguments
        self.admin = int(admin_id)
        self.api_key = api_key  # optional; only if the command needs it
        self.is_waiting_for_input = False
        self.is_waiting_for = User()
        self.has_scheduled_event = False
        self.is_always_listening = is_always_listening
        self.is_waiting_for_input = False
        self.default_language = language

    def reply(self, response):
        """Each command should have a reply function which accepts and returns
           a response object."""
        response.send_message.text = '<your text here>'  # text message example
        return response

    def listen(self, message):
        """Decides if the reply function of the commmand should be called.
           Accepts a message object and returns a truth value."""
        self.message = message
        self.arguments = self.get_arguments()
        self.data = shelve.open('data/chat_' + str(message.chat.id))
        if self.is_active() or self.is_always_listening or self.is_waiting_for_input:
            return True
        elif message.text.split()[0].lower().split('@')[0] == self.name:
            return True
        return False

    def is_active(self):
        """Returns whether the command is activated or not."""
        try:
            if self.data[self.name + '_active']:
                return True
        except:
            self.data[self.name + '_active'] = False
        return False

    def activate(self, boolean=True):
        """Activates or deactivates the command."""
        if boolean is False:
            self.data[self.name + '_active'] = False
        else:
            self.data[self.name + '_active'] = True

    def get_arguments(self):
        """Returns the command arguments."""
        if self.message.text and len(self.message.text.split()) > 1:
            return self.message.text.split(' ', 1)[1]

    def get_image(self, url):
        """Returns a string representation of an image."""
        return StringIO(urllib.urlopen(url).read()).getvalue()
