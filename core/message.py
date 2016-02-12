from user import User
from chat import Chat
from sticker import Sticker
from photo import Photo
from document import Document
from voice import Voice


class Message(object):
    """Message class for a Telegram message."""
    def __init__(self, message):
        self.id = message.get('message_id')
        self.date = message.get('date')
        self.text = message.get('text')
        self.chat = Chat(message.get('chat'))
        self.sender = User(message.get('from'))
        if message.get('forward_from'):
            self.forward_from = User(message.get('forward_from'))
        if message.get('sticker'):
            self.sticker = Sticker(message.get('sticker'))
        if message.get('photo'):
            self.photo = [Photo(ph) for ph in message.get('photo')]
        self.caption = message.get('caption')
        if message.get('document'):
            self.document = Document(message.get('document'))
        if message.get('voice'):
            self.voice = Voice(message.get('voice'))
        if message.get('reply_to_message'):
            self.reply_to_message = Message(message.get('reply_to_message'))

        # TODO: video, contact, location, user left chat, etc..

    def contains_command(self):
        if self.text and self.text.startswith('/') and len(self.text) > 1:
            self.command = self.text.split()[0].split('@')[0]
            return True
        return False
