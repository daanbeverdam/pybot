from reply_keyboard_markup import ReplyKeyboardMarkup
from reply_keyboard_hide import ReplyKeyboardHide
from force_reply import ForceReply


class Send(object):
    """Base class for Send objects."""
    def __init__(self):
        self.chat_id = None  # a valid response must always have chat_id
        self.reply_to_message_id = None  # optional
        self.reply_markup = ReplyKeyboardMarkup()  # custom keyboard (optional)
        self.reply_keyboard_hide = ReplyKeyboardHide()  # hide custom keyboard
        self.force_reply = ForceReply()  # force reply

    def to_dict(self):
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary['reply_markup'] = self.reply_markup.__dict__
        dictionary['reply_keyboard_hide'] = self.reply_keyboard_hide.__dict__
        dictionary['force_reply'] = self.force_reply.__dict__
        return dictionary
