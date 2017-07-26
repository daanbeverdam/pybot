from pybot.core.send_message import SendMessage
from pybot.core.forward_message import ForwardMessage
from pybot.core.send_photo import SendPhoto
from pybot.core.send_audio import SendAudio
from pybot.core.send_sticker import SendSticker
from pybot.core.send_document import SendDocument


class Response(object):
    """Represents a response from the bot."""

    def __init__(self, chat_id=None):
        self.send_message = SendMessage(chat_id)
        self.forward_message = ForwardMessage(chat_id)
        self.send_photo = SendPhoto(chat_id)
        self.send_audio = SendAudio(chat_id)
        self.send_sticker = SendSticker(chat_id)
        self.send_document = SendDocument(chat_id)
        # TODO: send_location, etc..
