from pybot.core.command import Command


class StatusCommand(Command):

    def reply(self, response):
        bot = self.helper.get_self()
        response.send_message.text = self.dialogs['reply'] % (bot.first_name, bot.id, self.message.chat.id)
        return response
