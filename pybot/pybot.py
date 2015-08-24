import commands.putin
import message
import config

class PyBot(object):
    commands = {
        'bbq' : commands.bbq.BBQCommand,
        'putin': commands.putin.PutinCommand
    }

    TOKEN = config.TEST_TOKEN
    BASE_URL = 'https://api.telegram.org/bot' + TOKEN + '/'

    def __init__(self, name, api_key):
        self.name = name
        self.api_key = api_key

    def run(self):
        while True:
            self.check_for_updates()

    def check_for_updates(self):
        response = get_updates()

        if response['ok']:
            pass
        else:
            log_message('Invalid reponse')

    def reply(self, chat_id, message = None, photo = None, document = None, location = None, preview_disabled = True, 
        caption = None):
        if message:
            response = urllib2.urlopen(BASE_URL + 'sendMessage', urllib.urlencode({
                'chat_id': str(chat_id),
                'text': message,
                'disable_web_page_preview': preview_disabled
            })).read()
        elif photo:
            response = multipart.post_multipart(BASE_URL + 'sendPhoto', [
                ('chat_id', str(chat_id)),
            ], [
                ('photo', 'photo.jpg', photo),
            ])
        elif document:
            response = multipart.post_multipart(BASE_URL + 'sendDocument', [
                ('chat_id', str(chat_id)),
            ], [
                ('document', 'document', document),
            ])
        elif location:
            response = urllib2.urlopen(BASE_URL + 'sendLocation', urllib.urlencode({
                'chat_id': str(chat_id),
                'latitude': location[0],
                'longitude': location[1]
            })).read()
        else:
            logging.error('no msg or img specified')
            response = None

    def reply_markup(self, chat_id, message, keyboard = None, selective = False, force_reply = False, message_id = None, 
        resize = True, one_time = True, disable_preview = True):
        if keyboard:
            reply_markup = ({'keyboard': keyboard, 
                'resize_keyboard': resize, 
                'one_time_keyboard': one_time,
                'selective': selective})
        else:
            reply_markup = ({'hide_keyboard': True,
                'selective': selective}])
        reply_markup = json.dumps(reply_markup)
        params = urllib.urlencode({
              'chat_id': str(chat_id),
              'text': msg.encode('utf-8'),
              'reply_markup': reply_markup,
              'disable_web_page_preview': disable_preview,
              (('reply_to_message_id': str(message_id)) if message_id == True else None),
              'force_reply' : force_reply,
        })
        resp = urllib2.urlopen(BASE_URL + 'sendMessage', params).read()

    def send_action(self, action)

