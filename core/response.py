from send_message import SendMessage
from forward_message import ForwardMessage
from send_photo import SendPhoto
from send_audio import SendAudio
from send_sticker import SendSticker


class Response(object):
    """Represents a response from the bot."""
    def __init__(self):
        self.send_message = SendMessage()
        # self.forward_message = ForwardMessage()
        # self.send_photo = SendPhoto()
        # self.send_audio = SendAudio()
        # self.sticker = SendSticker()

        # # Document:
        # self.document = None  # file_id or string representation of document
        # # Sticker:
        # # Video:
        # self.video = None  # file_id or string representation of video
        # # self.caption and self.duration also available for videos
        # self.voice = None  # file_id or string representation of voice message
        # # self.self.duration also available for voice
        # # Location:
        # self.latitude = None
        # self.longitude = None
        # # Reply to and keyboard markups are available for all of the above:
