from pybot.core.command import Command
import operator
from pybot.helpers.kudos import KudosHelper
from pybot.helpers.core import CoreHelper


class KudosCommand(Command):

    def reply(self, response):
        if self.message.text:
            reply = self.parse(self.message.text)
            if reply:
                response.send_message.text = reply
                return response

    def parse(self, text):
        helper = KudosHelper()
        reply = None
        if text.split()[0].split('@')[0] == self.name:
            if not self.arguments:
                reply = self.get_total_overview()
            else:
                user = helper.get_user_by_name(self.arguments, self.message.chat)
                if user and user.id == self.message.sender.id:
                    reply = self.dialogs['shame_on_you']
                elif user:
                    helper.mutate_kudos(user, self.message.chat, +1)
                    reply = self.get_user_overview(user)
                else:
                    reply = self.dialogs['not_in_chat'] % self.arguments
        if self.message.reply_to_message:
            result = self.parse_kudo_count(text)
            if result:
                no_of_kudos = result[0]
                trigger = result[1]
                appendix = self.get_special_message(trigger)
                user = self.message.reply_to_message.sender
                if user.id == self.message.sender.id:
                    reply = self.dialogs['shame_on_you']
                else:
                    helper.mutate_kudos(user, self.message.chat, no_of_kudos)
                    reply = self.get_user_overview(user, no_of_kudos) + appendix
        return reply

    def parse_kudo_count(self, text):
        sequences = {1: [u'\U0001F199', u'\U0001F51D', u'\U00002B06', '+1'],
                     -1: [u'\U00002B07', '-1'],
                     2: [u'\U0001F525'],
                     -2: [u'\U0001F4A9']}
        for kudo_count, triggers in sequences.items():
            for trigger in triggers:
                if trigger in text:
                    return (kudo_count, trigger)
        return None

    def get_total_overview(self):
        helper = KudosHelper()
        overview = helper.get_kudos_overview(self.message.chat)
        if overview:
            reply = self.dialogs['kudo_overview']
            overview.sort(key=lambda x: x[1], reverse=True)
            counter = 1
            for entry in overview:
                reply += "\n%s: %i" % (entry[0], entry[1])
                if counter == 1:
                    reply += ' \U0001F451'
                elif counter == len(overview) and len(overview) > 1:
                    reply += ' \U0001F480'
                counter += 1
        else:
            reply = self.dialogs['no_kudos']
        return reply

    def get_user_overview(self, user, kudos_given=1):
        helper = KudosHelper()
        kudo_count = helper.get_kudo_count(user, self.message.chat,)
        if abs(kudos_given) == 1:
            return self.dialogs['kudo_given'] % (user.first_name, kudo_count)
        return self.dialogs['kudos_given'] % (kudos_given, user.first_name, kudo_count)

    def get_special_message(self, trigger):
        messages = {u'\U0001F525': u'\U0001F525',
                    u'\U0001F4A9': u'\U0001F4A9'}
        message = messages.get(trigger)
        if message:
            return ' ' + message
        return ''
