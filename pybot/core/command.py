import shelve
import traceback
import io
import urllib
from pybot.core.response import Response
from pybot.core.user import User
from pybot.helpers.core import CoreHelper


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
        self.is_waiting_for = User()
        self.has_scheduled_event = False
        self.is_always_listening = is_always_listening
        self.is_waiting_for_input = False  # TODO: make this a function which consults the database
        self.default_language = language
        self.helper = CoreHelper()

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
        if self.is_active() or self.is_always_listening or self.is_waiting_for_input:
            return True
        elif message.text and message.text.split()[0].lower().split('@')[0] == self.name:
            return True
        return False

    def cancel(self, response):
        """Cancels the command."""
        if self.is_waiting_for_input or self.is_active():
            self.is_waiting_for_input = False
            self.activate(False)
            response.send_message.text = "OK, no worries."
            return response
        return None

    def done(self, response):
        """Tells the command the user is done."""
        return None

    def get_help(self, response):
        """Returns information on how to use the command."""
        response.send_message.text = self.usage
        return response

    def is_active(self):
        """Returns whether the command is activated or not."""
        # TODO: database check

    def activate(self, boolean=True):
        """Activates or deactivates the command."""
        # TODO: database set

    def chunk(self, text):
        """Chunks text if length exceeds Telegrams character limit. Returns list of chunks."""
        # TODO: move to bot.py?
        max_length = 4096
        chunks_needed = len(text) / max_length + 1

        if chunks_needed > 0:
            chunks = []
            x = 0

            for i in range(chunks_needed):

                chunks.append(text[max_length * x:max_length * (x + 1)])
                x += 1

            return chunks

        return [text]

    def get_arguments(self):
        """Returns the command arguments."""
        if self.message.text and len(self.message.text.split()) > 1:
            return self.message.text.split(' ', 1)[1]

    def to_string(self, url):
        """Returns a string representation of a document. Accepts url."""
        return io.StringIO(urllib.urlopen(url).read()).getvalue()
