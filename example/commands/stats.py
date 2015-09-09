from pybot.command import Command


class StatsCommand(Command):

    def reply(self):
        log = json.loads(open('json.log','r').read())
        reply = self.scan_entries(log)
        return {'message': reply}

    def scan_entries(self, log):
        relevant_entries = []
        for entry in log:
            chat_id = entry['message']['chat']['id']
            if chat_id == self.chat_id:
                relevant_entries.append(entry['message'])
        return self.calculate_statistics(relevant_entries)

    def calculate_statistics(self, entries):
        for message in entries:
            text = message.get('text')
            sender = message['from']
            sender_id = sender['id']
            first_name_sender = sender['first_name']
        return self.format()

    def format(self):
        # format reply
        pass





