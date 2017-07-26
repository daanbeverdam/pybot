from pybot.core.reply_keyboard_markup import ReplyKeyboardMarkup
import json


class Send(object):
    """Base class for Send objects."""

    def __init__(self, chat_id=None):
        self.chat_id = chat_id  # a valid response must always have chat_id
        self.reply_to_message_id = None
        self.force_reply = False
        self.reply_markup = ReplyKeyboardMarkup()

    def to_dict(self):
        """Returns a copy of self as dictionary."""
        self.encode_text()
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary['reply_markup'] = {}
        dictionary['reply_markup'].update(self.reply_markup.__dict__)

        if dictionary['reply_markup']['hide_keyboard']:
            del dictionary['reply_markup']['keyboard']  # keyboard and hide_keyboard can't co-exist
        elif not dictionary['reply_markup']['hide_keyboard'] and not dictionary['reply_markup']['keyboard']:
            del dictionary['reply_markup']  # delete reply_markup if it's not necessary

        if dictionary.get('reply_markup'):
            dictionary['reply_markup'] = json.dumps(dictionary['reply_markup'])

        # Telegram now validates data, so empty dictionary items need to be removed.
        unnecessary_keys = [key for key, value in dictionary.iteritems() if not value]

        for key in unnecessary_keys:
            del dictionary[key]

        return dictionary

    def get_files(self):
        """Returns name and media file as tuple. Used for multipart/form-data request."""
        media_types = ['photo', 'sticker', 'document', 'audio']
        dictionary = self.to_dict()
        files = {}

        for key in dictionary:

            if key in media_types and dictionary.get('name'):
                files[key] = (dictionary['name'], dictionary[key])

            elif key in media_types and dictionary.get('title'):
                files[key] = (dictionary['title'], dictionary[key])

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

        return data

    def encode_text(self, encoding='utf-8'):
        """Encodes all string variables to utf-8."""
        media_types = ['photo', 'sticker', 'document', 'audio']
        for key in self.__dict__:

            if isinstance(self.__dict__[key], basestring) and key not in media_types:
                self.__dict__[key] = self.__dict__[key].encode(encoding)

        if self.__dict__.get('reply_markup') and self.__dict__.get('reply_markup').keyboard:

            for l in self.__dict__['reply_markup'].keyboard:

                for i in l:
                    i = i.encode(encoding)
