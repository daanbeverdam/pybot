from core.command import Command
from core.response import Response


class EchoCommand(Command):

    def reply(self):
        self.response.send_message.text = self.arguments
        return self.response
