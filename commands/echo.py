from core.command import Command
from core.response import Response


class EchoCommand(Command):

    def reply(self, response):
        if self.message.sticker:
            respons.send_sticker.sticker = message.sticker
        elif self.message.text:
            response.send_message.text = self.arguments
        # self.response.send_message.reply_markup.keyboard = [['a','b']]
        # self.response.send_message.reply_markup.hide_keyboard = True
        return response
