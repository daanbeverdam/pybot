from core.command import Command


class CancelCommand(Command):
    """Command that returns giphy gifs to the user."""
    def reply(self, response):
        response.send_message.text = self.dialogs['reply'] % 'EVERYTHING'
        return response
