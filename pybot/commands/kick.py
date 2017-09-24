from pybot.core.command import Command
from pybot.libraries.requests import Requests
from pybot.helpers.kick import KickHelper
import math
import datetime


class KickCommand(Command):

    def reply(self, response):
        if self.arguments and not self.is_active():
            response = self.start_vote(response)
        elif self.is_active():
            response = self.check_vote(response)
        return response

    def cancel(self, response):
        """Cancels the command."""
        if self.is_active():
            response.send_message.text = self.dialogs['cancel']
            return response
        return None

    def start_vote(self, response):
        helper = KickHelper()
        user = helper.get_user_by_name(self.arguments, self.message.chat)
        if user:
            requests = Requests()
            no_of_members = requests.get_chat_members_count(self.message.chat)  # including bot
            required_no = math.ceil(no_of_members / 2)
            response.send_message.text = self.dialogs['start_vote'] % (user.first_name if not user.last_name else user.first_name + ' ' + user.last_name, required_no)
            response.send_message.reply_markup.keyboard = [['Yes', 'No']]
            response.send_message.force_reply = True
            response.send_message.reply_markup.one_time_keyboard = True
            helper.create_entry(self.message.chat, user, required_no)
            self.activate()
        else:
            response.send_message.text = self.dialogs['not_found']
        return response

    def check_vote(self, response):
        if self.message.text == 'Yes' or self.message.text == 'No':
            helper = KickHelper()
            if not helper.has_voted(self.message.chat, self.message.sender):
                helper.register_vote(self.message.chat, self.message.sender, self.message.text)
                vote_results = helper.get_vote_results(self.message.chat)
                response.send_message.text = self.dialogs['vote_recorded'] % vote_results
                response.send_message.reply_markup.hide_keyboard = True
                decision = helper.get_vote_descision(self.message.chat)
                if decision == 'kick':
                    requests = Requests()
                    user = helper.get_to_be_kicked_user(self.message.chat)
                    full_name = user.first_name if not user.last_name else user.first_name + ' ' + user.last_name
                    timestamp = self.get_timestamp(1)  # kick time is set to 1 minute
                    result = requests.kick_chat_member(self.message.chat, user, timestamp)
                    self.activate(False)
                    helper.remove_entry(self.message.chat)
                    if result['kicked']:
                        response.send_message.text = self.dialogs['user_kicked'] % full_name
                    else:
                        response.send_message.text = self.dialogs['kick_not_possible'] % (full_name, result['text'])
                elif decision == 'keep':
                    user = helper.get_to_be_kicked_user(self.message.chat)
                    full_name = user.first_name if not user.last_name else user.first_name + ' ' + user.last_name
                    response.send_message.text = self.dialogs['user_kept'] % full_name
                    self.activate(False)
                    helper.remove_entry(self.message.chat)
                return response

    def get_timestamp(self, minutes_from_now):
        current_time = datetime.datetime.now(datetime.timezone.utc)
        timestamp = current_time.timestamp()
        timestamp = timestamp + (minutes_from_now * 60)
        return timestamp
