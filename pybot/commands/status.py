from pybot.core.command import Command


class StatusCommand(Command):

    def reply(self, response):
        response.send_message.text = self.dialogs['reply']
        return response
