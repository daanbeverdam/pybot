from pybot.command import Command
import re
import json
import collections


class StatsCommand(Command):

    def reply(self):
        log = json.loads(open('json.log','r').read())
        reply = self.scan_entries(log)
        return {'message': reply}

    def scan_entries(self, log):
        relevant_entries = []
        for entry in log:
            chat_id = entry['message']['chat']['id']
            if chat_id == self.message.chat_id:
                relevant_entries.append(entry['message'])
        return self.calculate_statistics(relevant_entries)

    def calculate_statistics(self, entries):
        stat_dict = {}
        all_words = ''
        all_commands = ''
        for message in entries:
            text = message.get('text')
            if not text.startswith('/'):
                all_words += ' ' + text.lower()
            if text.startswith('/'):
                all_commands += ' ' + text
            sender = message['from']
            first_name_sender = sender['first_name']
            stat_dict.setdefault(first_name_sender, []).append(text)
        total_words = len(all_words.split(' '))
        words = re.findall(r'\w+', all_words)
        commands = re.findall(r'/\w+', all_commands)
        words = collections.Counter(words)
        commands = collections.Counter(commands)
        most_active_user = {'Nobody': []}
        for user in stat_dict.keys():
            if len(stat_dict[user]) > len(most_active_user.values()[0]):
                most_active_user = {user: stat_dict[user]}
        total_messages = len(entries)
        most_used_commands = commands.most_common(3)
        most_used_words = words.most_common(3)
        return self.dialogs['reply'] % (total_messages,
            most_used_commands[0][0], most_used_commands[0][1],
            most_used_commands[1][0], most_used_commands[1][1],
            most_used_commands[2][0], most_used_commands[2][1],
            most_active_user.keys()[0], len(most_active_user.values()[0]))





