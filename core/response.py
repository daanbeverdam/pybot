from send_message import SendMessage
from forward_message import ForwardMessage
from send_photo import SendPhoto
from send_audio import SendAudio
from send_sticker import SendSticker


class Response(object):
    """Represents a response from the bot."""

    def __init__(self, chat_id=None):
        self.send_message = SendMessage(chat_id)
        self.forward_message = ForwardMessage(chat_id)
        self.send_photo = SendPhoto(chat_id)
        self.send_audio = SendAudio(chat_id)
        self.send_sticker = SendSticker(chat_id)

        # TODO: send_document, send_location, etc..
