from pybot.command import Command
import os


class HelpCommand(Command):

    def reply(self):
        if self.arguments() == 'help':
            return {'message': self.usage}
        reply = self.dialogs['reply']
        command_list = []
        for name in os.listdir(os.path.dirname(os.path.abspath(__file__))):
            if name.endswith('.py') and name != '__init__.py':
                command_list.append('/' + name[:-3])
        reply += '\n' + '\n'.join(map(str, command_list))
        return {'message': reply}
