import config
from pybot.command import Command


class HelpCommand(Command):

    def reply(self):
        if self.arguments() == 'help':
            return {'message': self.usage}
        for command in config.COMMAND_LIST:
            self.reply_text += '\n/' + command.name
        return {'message': self.reply_text}
