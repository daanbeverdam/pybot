from pybot.core.message import Message
from pybot.core.response import Response
from pybot.helpers.core import CoreHelper
from pybot.core.user import User
from pybot.env import ROOT_DIR
import requests
import json
import urllib
import traceback
import os


class PyBot(object):
    """Main class that handles incoming messages appropriately."""

    def __init__(self, name, token, dialogs, commands, database):
        self.name = name
        self.token = token
        self.base_url = 'https://api.telegram.org/bot' + self.token + '/'
        self.helper = CoreHelper()
        self.dialogs = dialogs
        self.commands = commands
        self.command_names = [command.name for command in self.commands] + ['/cancel', '/done']

    def check_dirs(self):
        """Checks if the needed directories exist and creates them if they don't."""
        if not os.path.exists(ROOT_DIR + '/logs'):
            os.makedirs(ROOT_DIR + '/logs')
            print("Logs folder created")

    def self_check(self):
        """Checks self."""
        self.helper.check_db()
        self.helper.save_self(self.get_me())
        pass  # TODO: check for server updates etc.

    def run(self):
        """Main loop of the bot."""
        self.check_dirs()
        self.self_check()
        print("Bot started...")
        while True:
            try:
                self.check_for_updates()
            except KeyboardInterrupt:
                print("Keyboard interrupt! Bot stopped.")
                break
            except:
                self.log(traceback.format_exc(), 'error')

    def check_for_updates(self):
        """Checks for updates via long polling."""
        offset = self.helper.get_offset()
        parameters = {'timeout': 30, 'limit': 100, 'offset': offset}
        update_url = self.base_url + 'getUpdates'
        request = urllib.request.urlopen(update_url + '?' + urllib.parse.urlencode(parameters))
        update = json.loads(request.read())
        if update['ok'] and update['result']:
            self.helper.set_offset(int(update['result'][-1]['update_id'] + 1))
            for result in update['result']:
                message = Message(result['message'])
                try:
                    self.log(result, 'json')
                    self.log(self.name + " received a message from " + message.sender.first_name +
                             " in chat " + str(message.chat.id) + ".")
                    self.track(message)
                except:  # catch exceptions in logging/collecting, so it doesn't interfere with functionality
                    self.log(traceback.format_exc(), 'error')
                self.handle(message)
        elif not update['ok']:
            self.log("Couldn't get correct response! Update not OK.", 'error')

    def handle(self, message):
        """Handles incoming messages by looping through the commands."""
        for command in self.commands:
            response = Response(message.chat.id)
            if message.text:
                first_word = message.text.split()[0].split('@')[0]
            else:
                first_word = None
            if command.listen(message):
                try:
                    if first_word == '/cancel':
                        response = command.cancel(response)
                    elif first_word == '/done':
                        response = command.done(response)
                    elif command.requires_arguments and not command.arguments and not command.is_active():
                        response = Response(message.chat.id)
                        response.send_message.text = self.dialogs['input'] % command.name
                    elif command.arguments and command.arguments.lower() == 'help' and message.text.split()[0] == command.name:
                        response = command.get_help(response)
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

    def log(self, entry, log_type='readable', file_name=None, log_dir=ROOT_DIR + '/logs/'):
        """Logs entries into their respective log files."""
        if file_name:
            entry = entry.replace('\n', ' ')
            with open(log_dir + file_name, 'a') as log:
                log.write(entry + '\n')
        elif log_type in ['readable', 'error']:
            entry = entry.replace('\n', ' ')
            with open(log_dir + log_type + '.log', 'a') as log:
                log.write(entry + '\n')
            print(entry)  # readable responses also get printed to the terminal
        elif log_type in ['json', 'response']:
            with open(log_dir + log_type + '.log', 'a') as log:
                log.write(json.dumps(entry) + '\n')
        else:
            self.log("Error! Please specify correct log_type or file_name.", 'error')

    def track(self, message):
        """Keeps track of chats and users. Updates database."""
        if not self.helper.is_known(message.chat, message.sender):
            self.helper.save_user_chat(user=message.sender, chat=message.chat)

    def reply(self, response):
        """Sends response to user, accepts a response object."""
        request_url = self.base_url
        files = None
        if response.send_message.text:
            request_url += 'sendMessage'
            parameters = response.send_message.to_dict()
            self.log(self.name + " sent a message to chat " + str(response.send_message.chat_id) + ".")
        elif response.forward_message.from_chat_id:
            request_url += 'forwardMessage'
            parameters = response.forward_message.to_dict()
            self.log(self.name + " forwarded a message to chat " + str(response.send_message.chat_id) + ".")
        elif response.send_photo.photo:
            request_url += 'sendPhoto'
            if not response.send_photo.name:
                response.send_photo.name = 'photo.jpg'
                self.log("No filename was specified, using 'photo.jpg'. Please specify filenames!", 'error')
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
            files = response.send_document.get_files()
            data = response.send_document.get_data()
            self.log(self.name + " sent a document to chat " + str(response.send_message.chat_id) + ".")
        elif response.send_audio.audio:
            request_url += 'sendAudio'
            files = response.send_audio.get_files()
            data = response.send_audio.get_data()
            self.log(self.name + " sent an audio file to chat " + str(response.send_message.chat_id) + ".")
        else:
            self.log('No valid response!', 'error')
            return None
        if files:
            # Files should be sent via a multipart/form-data request.
            r = requests.post(request_url, files=files, data=data)
        else:
            r = requests.get(request_url, params=parameters)
        r = json.loads(r.text)
        self.log(r, 'response')

    def get_me(self):
        update_url = self.base_url + 'getMe'
        request = urllib.request.urlopen(update_url)
        update = json.loads(request.read())
        if update['ok'] and update['result']:
            result = update['result']
            return User(id=result['id'], first_name=result['first_name'], username=result['username'])

    def collect(self, message):
        pass

    # def send_action(self, chat_id, action):
    #     act = urllib.urlopen(self.base_url + 'sendChatAction',
    #                           urllib.urlencode({
    #                            'chat_id': str(chat_id),
    #                            'action': str(action)
    #                            })).read()
    #     self.log('Bot sent action "' + action + '" to ' + str(chat_id) + '.')
    # )
