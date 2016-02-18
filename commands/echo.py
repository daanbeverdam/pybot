from core.command import Command
from core.response import Response


class EchoCommand(Command):
    """Command that returns the message sent by the user."""
    
    def reply(self, response):
        
        if self.message.sticker:
            response.send_sticker.sticker = self.message.sticker.file_id
        elif self.message.text:
            response.send_message.text = self.arguments

        return response
