from core.command import Command


class StatusCommand(Command):

    def reply(self, response):
        return {'message': self.dialogs['reply']}
