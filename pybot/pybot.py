from message import Message
import multipart
import time
import json
import urllib
import urllib2
import shelve
import traceback
import os


class PyBot(object):

    def __init__(self, name, token, dialogs, commands):
        self.name = name
        self.token = token
        self.base_url = 'https://api.telegram.org/bot' + self.token + '/'
        self.dialogs = dialogs
        self.commands = commands
        self.update_interval = 0.8

    def check_dirs(self):
        if not os.path.exists('data'):
            os.makedirs('data')
            print "data folder created"

    def run(self):
        self.check_dirs()
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
        response = urllib2.urlopen(self.base_url + 'getUpdates',
            urllib.urlencode({
            'limit': 50,
            'offset': offset,
            })).read()
        body = json.loads(response)
        if body['ok'] and body['result'] != []:
            data['offset'] = body['result'][-1]['update_id'] + 1
            data.close()
            for result in body['result']:
                self.log(json_entry=result)
                message = Message(result['message'])
                self.handle_message(message)
        elif body['ok'] == False:
            self.log('Invalid response!')

    def handle_message(self, message):
        self.log(message.first_name_sender + ' sent "' + message.text +
                 '" in chat ' + str(message.chat_id) + '.')
        for command in self.commands:
            if command.listen(message) == 'help':
                reply = self.reply(message.chat_id, command.usage)
            elif command.listen(message):
                try:
                    reply = command.reply()
                    if 'keyboard' in reply:
                        self.reply_markup(message.chat_id, **reply)
                    else:
                        self.reply(message.chat_id, **reply)
                except:
                    traceback.print_exc()
                    self.reply(message.chat_id,
                               self.dialogs['command_failed'] % command.name)
        if self.name.lower() in message.text.lower():
            self.reply(message.chat_id, 'Hi ' + message.first_name_sender + '!')

    def log(self, entry=None, json_entry=None):
        if entry:
            print(str(entry.encode('utf-8').replace('\n', ' ')))
            with open('readable.log', 'a') as log:
                log.write(entry.replace('\n', ' ').encode('utf-8') + '\n')
        elif json_entry:
            with open('json.log', mode='a') as log:
                json.dump(json_entry, log, indent=2)

    def reply(self, chat_id, message=None, photo=None, document=None, gif=None,
              location=None, preview_disabled=True, caption=None):
        if message:
            response = urllib2.urlopen(self.base_url + 'sendMessage',
                urllib.urlencode({
                'chat_id': str(chat_id),
                'text': message.encode('utf-8'),
                'disable_web_page_preview': str(preview_disabled)
            })).read()
            self.log('Bot sent reply "' + message + '" to ' + str(chat_id) + '.')
        elif photo:
            self.send_action(chat_id, 'upload_photo')
            response = multipart.post_multipart(self.base_url + 'sendPhoto', [
                ('chat_id', str(chat_id)),
            ], [
                ('photo', 'photo.jpg', photo),
            ])
            self.log('Bot sent photo to ' + str(chat_id) + '.')
        elif gif or document:
            self.send_action(chat_id, 'upload_document')
            response = multipart.post_multipart(self.base_url + 'sendDocument', [
                ('chat_id', str(chat_id)),
            ], [
                ('document', ('image.gif' if gif else 'document.file') , (gif if gif else document)),
            ])
            self.log('Bot sent document to ' + str(chat_id) + '.')
        elif location:
            response = urllib2.urlopen(self.base_url + 'sendLocation', urllib.urlencode({
                'chat_id': str(chat_id),
                'latitude': location[0],
                'longitude': location[1]
            })).read()
            self.log('Bot sent location to ' + str(chat_id) + '.')

    def reply_markup(self, chat_id, message, keyboard=None, selective=False,
                     force_reply=False, message_id=None, resize=True,
                     one_time=True, disable_preview=True):
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
              'text': message,
              'reply_markup': reply_markup,
              'force_reply' : force_reply,
              'disable_web_page_preview': disable_preview,
              'reply_to_message_id': str(message_id)
        })
        response = urllib2.urlopen(self.base_url + 'sendMessage', params).read()
        self.log('Bot sent markup: ' + '"' + message + '" ' + str(keyboard) +
                 ' to ' + str(chat_id) + '.')

    def send_action(self, chat_id, action):
        act = urllib2.urlopen(self.base_url + 'sendChatAction', urllib.urlencode({
            'chat_id': str(chat_id),
            'action': str(action)
        })).read()
        self.log('Bot sent action "' + action + '" to ' + str(chat_id) + '.')
