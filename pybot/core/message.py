from pybot.core.user import User
from pybot.core.chat import Chat
from pybot.core.sticker import Sticker
from pybot.core.photo import Photo
from pybot.core.document import Document
from pybot.core.voice import Voice


class Message(object):
    """Represents a Telegram message."""

    def __init__(self, message):
        self.id = message.get('message_id')
        self.date = message.get('date')
        self.text = message.get('text')
        self.chat = Chat(message.get('chat'))
        self.sender = User(message.get('from'))
        self.forward_from = message.get('forward_from')
        self.reply_to_message = message.get('reply_to_message')
        self.sticker = message.get('sticker')
        self.photo = message.get('photo')
        self.caption = message.get('caption')
        self.document = message.get('document')
        self.voice = message.get('voice')

        if self.forward_from:
            self.forward_from = User(message.get('forward_from'))
        if self.sticker:
            self.sticker = Sticker(message.get('sticker'))
        if self.photo:
            self.photo = [Photo(ph) for ph in message.get('photo')]
        if self.document:
            self.document = Document(message.get('document'))
        if self.voice:
            self.voice = Voice(message.get('voice'))
        if self.reply_to_message:
            self.reply_to_message = Message(message.get('reply_to_message'))

        # TODO: video, contact, location, user left chat, etc..

    def contains_command(self):
        if self.text and self.text.startswith('/') and len(self.text) > 1:
            self.command = self.text.split()[0].split('@')[0]
            return True
        return False
