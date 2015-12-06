from pybot.command import Command
from datetime import datetime


class Reminder(Command):

    def reply(self):
        tokens = self.arguments.split()
        reminder = analyze(tokens)
        scheduled_events = shelve.open('scheduled_events')
        try:
            l = scheduled_events[self.message.chat_id]
            l.append(reminder)
            scheduled_events[self.message.chat_id] = l
        else:
            scheduled_events[self.message.chat_id] = [reminder]
        scheduled.close()
        return {'message': self.dialogs['reminder_saved']}

    def analyze(self, tokens):
        reminder = {}
        date = None
        time = None
        current = datetime.now()
        current_time = str(time_stamp).split()[1] #hh:mm:ss.ssss
        for token in tokens:
            if '-' in token:
                date = tokens[0].split('-')
                day = int(date[0])
                month = int(date[1])
                if len(date) > 2:
                    year = int(date[2])
                else:
                    year = current.year
                reminder['date'] = (year, month, day)
                tokens.remove(token)
            elif ':' in token:
                time = token.split(':')
                hour = int(time[0])
                minute = int(time[1])
                reminder['time'] = (hour, minute)
                tokens.remove(token)
            elif 'tomorrow' in token or 'morgen' in token:
                delta = datetime.timedelta(days=1)
                new = current + delta
                reminder['date'] = (current.year, current.month, new.day)
                tokens.remove(token)
        if not time:
            reminder['time'] = (current.hour, current.minute)
        if not date:
            reminder['date'] = (current.year, current.month, current.day)
        reminder['text'] = ' '.join(tokens)
        return reminder
