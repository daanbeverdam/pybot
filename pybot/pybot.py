from message import Message
import config
import multipart
import time
import json
import urllib, urllib2
import shelve
import traceback

class PyBot():

    def __init__(self, name = config.BOT_NAME, token = config.TOKEN):
        self.name = name
        self.token = token
        self.base_url = 'https://api.telegram.org/bot' + self.token + '/'
        self.update_interval = 0.8

    def run(self):
        while True:
            try:
                self.check_for_updates()
                time.sleep(self.update_interval)
            except:
                traceback.print_exc()
                time.sleep(self.update_interval)

    def check_for_updates(self):
        data = shelve.open('main_data')
        try:
            offset = data['offset']
        except:
            offset = 0
        response = urllib2.urlopen(self.base_url + 'getUpdates', urllib.urlencode({
            'limit': 50,
            'offset': offset,
            })).read()
        body = json.loads(response)
        if body['ok'] and body['result'] != []:
            data['offset'] = body['result'][-1]['update_id'] + 1
            data.close()
            for result in body['result']:
                message = Message(result['message'])
                self.handle_message(message)
        elif body['ok'] == False:
            self.log('Invalid response!')

    def handle_message(self, message):
        self.log(message.first_name_sender + ' sent "' + message.text + '" in chat ' + 
            str(message.chat_id) + '.')
        if message.command:
            try:
                self.reply(message.chat_id, **message.command.reply)
            except: # doesn't work
                self.reply(message.chat_id, "Oeps, er ging iets mis. Type '/%s help' "
                "voor hulp bij het gebruik van dit commando." % message.command.name)
                traceback.print_exc()
        elif self.name.lower() in message.text.lower():
            self.reply(message.chat_id, 'Hoi ' + message.first_name_sender + '!')

    def log(self, entry):
        print(str(entry.encode('utf-8')))
        with open('pybot.log','a') as log:
            log.write(str(entry) + '\n')

    def reply(self, chat_id, message = None, photo = None, document = None, location = None, 
        preview_disabled = True, caption = None):
        if message:
            response = urllib2.urlopen(self.base_url + 'sendMessage', urllib.urlencode({
                'chat_id': str(chat_id),
                'text': message.encode('utf-8'),
                'disable_web_page_preview': str(preview_disabled)
            })).read()
            self.log('Sent reply "' + message + '" to ' + str(chat_id) + '.')
        elif photo:
            self.send_action(chat_id, 'upload_photo')
            response = multipart.post_multipart(self.base_url + 'sendPhoto', [
                ('chat_id', str(chat_id)),
            ], [
                ('photo', 'photo.jpg', photo),
            ])
            self.log('Sent photo to ' + str(chat_id) + '.')
        elif document:
            self.send_action(chat_id, 'upload_document')
            response = multipart.post_multipart(self.base_url + 'sendDocument', [
                ('chat_id', str(chat_id)),
            ], [
                ('document', 'document.*', document),
            ])
            self.log('Sent document to ' + str(chat_id) + '.')
        elif location:
            response = urllib2.urlopen(self.base_url + 'sendLocation', urllib.urlencode({
                'chat_id': str(chat_id),
                'latitude': location[0],
                'longitude': location[1]
            })).read()
            self.log('Sent location to ' + str(chat_id) + '.')
        else:
            self.log('Error: contents of message and/or chat id not correctly specified.')
            response = None

    def reply_markup(self, chat_id, message, keyboard = None, selective = False, force_reply = False, 
        message_id = None, resize = True, one_time = True, disable_preview = True):
        if keyboard:
            reply_markup = ({
                'keyboard': keyboard, 
                'resize_keyboard': resize, 
                'one_time_keyboard': one_time,
                'selective': selective
            })
        else:
            reply_markup = ({
                'hide_keyboard': True,
                'selective': selective
            })
        reply_markup = json.dumps(reply_markup)
        params = urllib.urlencode({
              'chat_id': str(chat_id),
              'text': message.encode('utf-8'),
              'reply_markup': reply_markup,
              'disable_web_page_preview': disable_preview,
              'reply_to_message_id': str(message_id) if message_id == True else None,
              'force_reply' : force_reply
        })
        response = urllib2.urlopen(self.base_url + 'sendMessage', params).read()
        self.log('Sent markup: ' + str(keyboard) + ' to ' + str(chat_id) + '.')

    def send_action(self, chat_id, action):
        act = urllib2.urlopen(self.base_url + 'sendChatAction', urllib.urlencode({
            'chat_id': str(chat_id),
            'action': str(action)
        })).read()
        self.log('Sent action "' + action + '" to ' + str(chat_id) + '.')
