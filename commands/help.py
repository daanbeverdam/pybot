from core.command import Command


class HelpCommand(Command):

    def reply(self, response):
        response.send_message.text = self.dialogs['reply']
        return response
