from core.command import Command


class StartCommand(Command):
    # Every bot should have a start command

    def reply(self, response):
        response.send_message.text = self.dialogs['reply']
        return response
