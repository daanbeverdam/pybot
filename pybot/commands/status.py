from pybot.core.command import Command
from pybot.helpers.core import CoreHelper


class StatusCommand(Command):

    def reply(self, response):
        helper = CoreHelper()
        bot = helper.get_self()
        response.send_message.text = self.dialogs['reply'] % (bot.first_name, bot.id, self.message.chat.id, self.message.sender.id)
        return response
