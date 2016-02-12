from send_message import SendMessage
from forward_message import ForwardMessage
from send_photo import SendPhoto
from send_audio import SendAudio
from send_sticker import SendSticker


class Response(object):
    """Represents a response from the bot."""
    def __init__(self, chat_id=None):
        self.chat_id = chat_id
        self.send_message = SendMessage(self.chat_id)
        self.forward_message = ForwardMessage(self.chat_id)
        self.send_photo = SendPhoto(self.chat_id)
        self.send_audio = SendAudio(self.chat_id)
        self.sticker = SendSticker(self.chat_id)

        # # Document:
        # self.document = None  # file_id or string representation of document
        # # Video:
        # self.video = None  # file_id or string representation of video
        # # self.caption and self.duration also available for videos
        # self.voice = None  # file_id or string representation of voice message
        # # self.self.duration also available for voice
        # # Location:
        # self.latitude = None
        # self.longitude = None
