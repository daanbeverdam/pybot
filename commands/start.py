from core.command import Command


class StartCommand(Command):
    # Every bot should have a start command

    def reply(self, response):
        return {'message': self.dialogs['reply']}
