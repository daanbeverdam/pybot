from reply_keyboard_markup import ReplyKeyboardMarkup
from reply_keyboard_hide import ReplyKeyboardHide
from force_reply import ForceReply
import json


class Send(object):
    """Base class for Send objects."""
    def __init__(self, chat_id=None):
        self.chat_id = chat_id  # a valid response must always have chat_id
        self.reply_to_message_id = None
        self.reply_markup = ReplyKeyboardMarkup()
        self.reply_keyboard_hide = ReplyKeyboardHide()
        self.force_reply = ForceReply()

    def to_dict(self):
        """Returns self as dictionary."""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary['reply_markup'] = self.reply_markup.__dict__
        dictionary['reply_keyboard_hide'] = self.reply_keyboard_hide.__dict__
        dictionary['force_reply'] = self.force_reply.__dict__
        return dictionary

    def to_tuples(self):
        """Returns self as array of tuples."""
        tuples = self.to_dict().items()
        return tuples

    def get_files(self):
        """Returns name and media file as tuple. Used for multipart/form-data request."""
        media_types = ['photo', 'sticker', 'document', 'audio']
        dictionary = self.to_dict()
        files = {}
        for key in dictionary:
            if key in media_types:
                files[key] = (dictionary['name'], dictionary[key])
        return files

    def get_data(self):
        """Returns attributes of self as dictionary, excluding media file.
        Used for multipart/form-data request."""
        media_types = ['photo', 'sticker', 'document', 'audio']
        dictionary = self.to_dict()
        data = {}
        for key in dictionary:
            if key not in media_types:
                data[key] = dictionary[key]
        data['reply_markup'] = json.dumps(data['reply_markup'])
        return data
