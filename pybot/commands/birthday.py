from pybot.core.command import Command
from pybot.helpers.birthday import BirthdayHelper
from dateutil.parser import parse
from pybot.etc import config
import datetime
from pybot.core.response import Response


class BirthdayCommand(Command):

    def reply(self, response):
        helper = BirthdayHelper()
        birthday = helper.get_birthday(self.message.chat, self.message.sender)
        if birthday:
            response.send_message.text = self.dialogs['birthday'] % birthday
        elif self.get_arguments() and not birthday:
            birthday = self.get_arguments()
            if self.is_valid_date(birthday):
                birthday = parse(birthday, dayfirst=True).strftime('%d-%m-%Y')  # Sorry EN users!
                helper.save_birthday(self.message.chat, self.message.sender, birthday)
                reply = self.dialogs['saved'] + ' ' + self.dialogs['birthday'] % birthday
                response.send_message.text = reply
            else:
                response.send_message.text = self.dialogs['not_valid'] % "DD-MM-YYYY"
        return response

    def get_scheduled(self):
        """Returns birthday notifications when appropriate."""
        responses = []
        today = datetime.date.today().strftime('%d-%m')
        helper = BirthdayHelper()
        birthdays = helper.get_birthdays(today)
        if birthdays:
            for birthday in birthdays:
                if self.birthday_is_today(birthday[2]) and not self.is_today(birthday[3]):
                    full_date = datetime.date.today().strftime('%d-%m-%Y')
                    helper.set_notified_at(birthday[0], birthday[1], full_date)
                    responses.append(self.get_notification(birthday[0], birthday[1]))
        return responses

    def get_notification(self, chat_id, user_id):
        """Generates birthday notification response."""
        response = Response(chat_id)
        helper = BirthdayHelper()
        user = helper.get_user(user_id)
        response.send_message.text = self.dialogs['happy_birthday'] % (user.first_name, user.last_name if
                                                                       user.last_name else '')
        return response

    def is_today(self, date):
        """Checks if a date string is today."""
        date = parse(date, dayfirst=True).strftime('%d-%m-%Y')
        today = datetime.date.today().strftime('%d-%m-%Y')
        if date == today:
            return True
        return False

    def birthday_is_today(self, date):
        """Checks if a date string is today, ignoring the year. Returns truth value."""
        date = parse(date, dayfirst=True).strftime('%d-%m')
        today = datetime.date.today().strftime('%d-%m')
        if date == today:
            return True
        return False

    def is_valid_date(self, date):
        try:
            parse(date)
            return True
        except:
            return False
