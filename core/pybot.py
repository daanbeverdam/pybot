from message import Message
from response import Response
import requests
import time
import json
import urllib
import urllib2
import shelve
import traceback
import os
from pymongo import MongoClient  # for accessing the database
from datetime import datetime


class PyBot(object):
    """Main class that handles incoming messages appropriately."""

    def __init__(self, name, token, dialogs, commands, database):
        self.name = name
        self.token = token
        self.db = MongoClient()[database]
        self.base_url = 'https://api.telegram.org/bot' + self.token + '/'
        self.dialogs = dialogs
        self.commands = commands
        self.command_names = [command.name for command in self.commands] + ['/cancel', '/done']

    def check_dirs(self):
        """Checks if the needed directories exist and creates them if they don't."""
        if not os.path.exists('data'):
            os.makedirs('data')
            print "Data folder created"

        if not os.path.exists('logs'):
            os.makedirs('logs')
            print "Logs folder created"

    def check_documents(self):
        """Checks if the required documents in the database exist."""
        if not self.db.main.find_one():
            self.db.main.insert_one({'offset': 0})

    def bind_db(self):
        """Binds database to commands."""
        for command in self.commands:
            command.db = self.db

    def run(self):
        """Main loop of the bot."""
        self.check_dirs()
        self.check_documents()
        self.bind_db()
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
        """Checks for updates via long polling."""
        offset = self.db.main.find_one()['offset']
        parameters = {'timeout': 30, 'limit': 100, 'offset': offset}
        update_url = self.base_url + 'getUpdates'
        request = urllib2.urlopen(update_url, urllib.urlencode(parameters))
        update = json.loads(request.read())

        if update['ok'] and update['result']:
            self.db.main.update({}, {
                '$set': {
                'offset': int(update['result'][-1]['update_id'] + 1)
                }})
            for result in update['result']:
                message = Message(result['message'])
                self.log(result, 'json')
                self.log(self.name + " received a message from " + message.sender.first_name +
                         " in chat " + str(message.chat.id) + ".")
                self.collect(message)
                self.handle(message)
        elif not update['ok']:
            self.log("Couldn't get correct response! Update not OK.", 'error')

    def handle(self, message):
        """Handles incoming messages by looping through the commands."""
        for command in self.commands:
            response = Response(message.chat.id)

            if command.listen(message):
                print command.name + ' activated!'

                try:

                    if message.text == '/cancel':
                        response = command.cancel(response)

                    elif message.text == '/done':
                        response = command.done(response)

                    elif command.is_waiting_for_input and command.is_waiting_for.id == message.sender.id:
                        command.arguments = message.text
                        command.is_waiting_for_input = False
                        response = command.reply(response)

                    elif command.requires_arguments and not command.arguments:
                        response = Response(message.chat.id)
                        command.is_waiting_for_input = True
                        command.is_waiting_for = message.sender
                        response.send_message.text = self.dialogs['input'] % command.name

                    else:
                        response = command.reply(response)

                except:
                    response.send_message.text = self.dialogs['command_failed'] % command.name
                    self.log(traceback.format_exc(), 'error')

                if isinstance(response, list):
                    for rsp in response:
                        self.reply(rsp)

                elif response:
                    self.reply(response)

        if message.contains_command() and message.command.lower() not in self.command_names:
            response = Response(message.chat.id)
            response.send_message.text = self.dialogs['no_such_command']
            self.reply(response)

    def log(self, entry, log_type='readable', file_name=None):
        """Logs entries into their respective log files."""
        if file_name:
            entry = entry.encode('utf-8').replace('\n', ' ')
            with open('logs/' + file_name, 'a') as log:
                log.write(entry + '\n')
        elif log_type in ['readable', 'error']:
            entry = entry.encode('utf-8').replace('\n', ' ')
            with open('logs/' + log_type + '.log', 'a') as log:
                log.write(entry + '\n')
            print entry  # readable responses also get printed to the terminal
        elif log_type in ['json', 'response']:
            with open('logs/' + log_type + '.log', 'a') as log:
                log.write(json.dumps(entry) + '\n')
        else:
            self.log("Error! Please specify correct log_type or file_name.", 'error')

    def reply(self, response):
        """Sends response to user, accepts a response object."""
        request_url = self.base_url
        files = None

        if response.send_message.text:
            request_url += 'sendMessage'
            parameters = response.send_message.to_dict()
            self.log(self.name + " sent '" + response.send_message.text + "' to chat " + str(response.send_message.chat_id) + ".")
        elif response.forward_message.from_chat_id:
            request_url += 'forwardMessage'
            parameters = response.forward_message.to_dict()
            self.log(self.name + " forwarded a message to chat " + str(response.send_message.chat_id) + ".")
        elif response.send_photo.photo:
            request_url += 'sendPhoto'
            if not response.send_photo.name:
                response.send_photo.name = 'photo.jpg'
            dictionary = response.send_photo.to_dict()
            files = response.send_photo.get_files()
            data = response.send_photo.get_data()
            self.log(self.name + " sent a photo to chat " + str(response.send_message.chat_id) + ".")
        elif response.send_sticker.sticker:
            request_url += 'sendSticker'
            parameters = response.send_sticker.to_dict()
            self.log(self.name + " sent a sticker to chat " + str(response.send_message.chat_id) + ".")
        elif response.send_document.document:
            request_url += 'sendDocument'
            if not response.send_document.name:
                self.log('File name not specified! This could cause issues.', 'error')
            dictionary = response.send_document.to_dict()
            files = response.send_document.get_files()
            data = response.send_document.get_data()
            self.log(self.name + " sent a document to chat " + str(response.send_message.chat_id) + ".")
        else:
            self.log('No valid response!', 'error')
            return None

        if files:
            # Files should be sent via a multipart/form-data request.
            r = requests.post(request_url, files=files, data=data)
            r = json.loads(r.text)
        else:
            # For text-based messages, a simple urlopen should do the trick.
            r = urllib2.urlopen(request_url, urllib.urlencode(parameters))
            r = json.loads(r.read())

        self.log(r['result'], 'response')

    def collect(self, message):
        """Stores statistics and user information in database."""
        user = message.sender.__dict__
        words = 0
        sticker = 0
        photo = 0
        document = 0
        command = None

        if message.text:
            tokens = message.text.split()
            words = len(tokens)
            command_list = [token for token in tokens if token in self.command_names]
            command = command_list[0] if len(command_list) > 0 else None
        elif message.sticker:
            sticker = 1
        elif message.photo:
            photo = 1
        elif message.document:
            document = 1

        query = {
            'id': message.chat.id
        }
        update = {
            '$inc': {
                'statistics.total_messages': 1,
                'statistics.total_words': words,
                'statistics.total_stickers': sticker,
                'statistics.total_photos': photo,
                'statistics.total_documents': document,
                'statistics.users.' + str(user['id']) + '.total_messages': 1,
                'statistics.users.' + str(user['id']) + '.total_words': words,
                'statistics.users.' + str(user['id']) + '.total_stickers': sticker,
                'statistics.users.' + str(user['id']) + '.total_photos': photo,
                'statistics.users.' + str(user['id']) + '.total_documents': document
            },
            '$set': {'users.' + str(user['id']): user}
        }

        if command:
            update['$inc']['statistics.commands.' + command] = 1

        self.db.chats.update(query, update, upsert=True)

    # def send_action(self, chat_id, action):
    #     act = urllib2.urlopen(self.base_url + 'sendChatAction',
    #                           urllib.urlencode({
    #                            'chat_id': str(chat_id),
    #                            'action': str(action)
    #                            })).read()
    #     self.log('Bot sent action "' + action + '" to ' + str(chat_id) + '.')
    # )
