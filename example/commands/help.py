from pybot.command import Command
import os


class HelpCommand(Command):

    def reply(self):
        if self.arguments() == 'help':
            return {'message': self.usage}
        reply = self.dialogs['reply']
        for name in os.listdir(os.path.dirname(os.path.abspath(__file__))):
            if name.endswith('.py') and name != '__init__.py':
                reply += '\n/' + name[:-3]
        return {'message': reply}
