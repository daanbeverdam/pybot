import requests
from message import Message
from response import Response
from multipart import post_multipart
import time
import json
import urllib
import urllib2
import shelve
import traceback
import os
from datetime import datetime


class PyBot(object):
    """Main class that handles incoming messages and replies appropriately."""
    def __init__(self, name, token, dialogs, commands):
        self.name = name
        self.token = token
        self.base_url = 'https://api.telegram.org/bot' + self.token + '/'
        self.dialogs = dialogs
        self.commands = commands
        self.reserved_names = ['cancel', 'results', 'done']  # TODO: make seperate commands
        self.command_names = [command.name for command in self.commands]
        self.is_waiting_for_input = False

    def check_dirs(self):
        if not os.path.exists('data'):
            os.makedirs('data')
            print "Data folder created"
        if not os.path.exists('logs'):
            os.makedirs('logs')
            print "Logs folder created"

    def run(self):
        self.check_dirs()
        print "Bot started..."
        while True:
            try:
                self.check_for_updates()
            except KeyboardInterrupt:
                print "Keyboard interrupt! Bot stopped."
                break
            except:
                self.log(traceback.format_exc(), 'error')

    def check_for_updates(self):
        self.main_data = shelve.open('data/main')
        offset = self.main_data.get('offset')
        parameters = {'timeout': 30, 'limit': 100, 'offset': offset}
        update_url = self.base_url + 'getUpdates'
        request = urllib2.urlopen(update_url, urllib.urlencode(parameters))
        update = json.loads(request.read())

        if update['ok'] and update['result']:
            self.main_data['offset'] = update['result'][-1]['update_id'] + 1
            self.main_data.close()
            for result in update['result']:
                message = Message(result['message'])
                self.handle(message)
                self.log(result['message'], 'json')

        elif not update['ok']:
            self.log("Couldn't get correct response! Update not OK.", 'error')

    # def check_for_scheduled_events(self):
    #     scheduled_events = shelve.open('scheduled_events')
    #     current = datetime.now()
    #     for chat_id in scheduled_events:
    #         for event in chat_id:
    #             if ((current.year, current.month, current.day) == event['date']
    #                     and (current.hour, current.minute) == event['time']):
    #                 self.reply(chat_id, event['text'])
    #     scheduled_events.close()

    def handle(self, message):
        for command in self.commands:
            
            if command.listen(message):
                
                if command.is_waiting_for_input and command.is_waiting_for.id == message.sender.id:
                    command.arguments = message.text
                    command.is_waiting_for_input = False
                    response = command.reply()
                
                if command.requires_arguments and not command.arguments:
                    command.response.send_message.text = self.dialogs['input'] % command.name
                    command.is_waiting_for_input = True
                    command.is_waiting_for = message.sender
                    response = command.response
                
                else:
                    response = command.reply()
                
                self.reply(response)

        if message.contains_command() and message.command.lower() not in self.command_names:
            response = Response(message.chat.id)
            response.send_message.text = self.dialogs['no_such_command']
            self.reply(response)

    def log(self, entry, log_type='readable', file_name=None):
        if file_name:
            entry = entry.encode('utf-8').replace('\n', ' ')
            with open('logs/' + file_name, 'a') as log:
                log.write(entry + '\n')

        elif log_type == 'readable' or log_type == 'error':
            entry = entry.encode('utf-8').replace('\n', ' ')
            with open('logs/' + log_type + '.log', 'a') as log:
                log.write(entry + '\n')

        elif log_type == 'json':
            with open('logs/json.log', 'a') as log:
                log.write(json.dumps(entry) + '\n')

        else:
            print "Error! Please specify correct log type or a file name."

        print entry

    def reply(self, response):
        """Sends responses to user, accept a response object."""
        request_url = self.base_url
        files = None

        if response.send_message.text:
            request_url += 'sendMessage'
            parameters = response.send_message.to_dict()
            self.log(self.name + ': ' + response.send_message.text + ' to chat ' + str(response.send_message.chat_id) + '.')

        elif response.forward_message.from_chat_id:
            request_url += 'forwardMessage'
            parameters = response.forward_message.to_dict()

        elif response.send_photo.photo:
            request_url += 'sendPhoto'
            if not response.send_photo.name:
                response.send_photo.name = 'photo.jpg'
            dictionary = response.send_photo.to_dict()
            files = response.send_photo.get_files()
            data = response.send_photo.get_data()
            print data
            parameters = [('chat_id', str(response.chat_id))]

        elif response.send_sticker.sticker:
            request_url += 'sendSticker'
            parameters = responses.send_sticker.to_dict()

        if files:
            # Files should be sent via a multipart/form-data request.
            r = requests.post(request_url, files=files, data=data)
        else:
            # For text-based messages, a simple urlopen should do the trick.
            r = urllib2.urlopen(request_url, urllib.urlencode(parameters))

    #     if message:
    #         response = urllib2.urlopen(self.base_url + 'sendMessage',
    #                                    urllib.urlencode()).read()
    #         self.log('Bot sent reply "' + message + '" to ' +
    #                  str(chat_id) + '.')
    #     elif photo:
    #         self.send_action(chat_id, 'upload_photo')
    #         parameters = [('chat_id', str(chat_id))]
    #         if caption:
    #             parameters.append(('caption', caption.encode('utf-8')))
    #         response = post_multipart(self.base_url + 'sendPhoto', parameters,
    #                                   [('photo', 'photo.jpg', photo)])
    #         self.log('Bot sent photo to ' + str(chat_id) + '.')
    #     elif gif or document:
    #         self.send_action(chat_id, 'upload_document')
    #         if gif:
    #             file_name = 'image.gif'
    #         else:
    #             file_name = str(file_name + extension)
    #         response = post_multipart(self.base_url + 'sendDocument',
    #                                   [('chat_id', str(chat_id))],
    #                                   [('document', (file_name),
    #                                    (gif if gif else document))])
    #         self.log('Bot sent document to ' + str(chat_id) + '.')
    #     elif location:
    #         response = urllib2.urlopen(self.base_url + 'sendLocation',
    #                                    urllib.urlencode({
    #                                     'chat_id': str(chat_id),
    #                                     'latitude': location[0],
    #                                     'longitude': location[1]
    #                                     })).read()
    #         self.log('Bot sent location to ' + str(chat_id) + '.')
    #
    # def reply_markup(self, chat_id, message, keyboard=None, selective=False,
    #                  force_reply=False, message_id=None, resize=True,
    #                  one_time=True, disable_preview=True):
    #     if keyboard:
    #         reply_markup = ({
    #             'keyboard': keyboard,
    #             'resize_keyboard': resize,
    #             'one_time_keyboard': one_time,
    #             'selective': selective
    #         })
    #     else:
    #         reply_markup = ({
    #             'hide_keyboard': True,
    #             'selective': selective
    #         })
    #     reply_markup = json.dumps(reply_markup)
    #     params = urllib.urlencode({
    #           'chat_id': str(chat_id),
    #           'text': message.encode('utf-8'),
    #           'reply_markup': reply_markup,
    #           'force_reply': force_reply,
    #           'disable_web_page_preview': disable_preview,
    #           'reply_to_message_id': str(message_id)
    #     })
    #     response = urllib2.urlopen(self.base_url + 'sendMessage',
    #                                params).read()
    #     self.log('Bot sent markup: ' + '"' + message + '" ' + str(keyboard) +
    #              ' to ' + str(chat_id) + '.')

    # def send_action(self, chat_id, action):
    #     act = urllib2.urlopen(self.base_url + 'sendChatAction',
    #                           urllib.urlencode({
    #                            'chat_id': str(chat_id),
    #                            'action': str(action)
    #                            })).read()
    #     self.log('Bot sent action "' + action + '" to ' + str(chat_id) + '.')
