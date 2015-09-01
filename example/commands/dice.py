import random
from pybot.command import Command


class DiceCommand(Command):

    def reply(self):
        if self.arguments() == 'help':
            return {'message': self.usage}
        elif self.arguments() == None:
            number_of_dice = 1
        else:
            number_of_dice = int(self.arguments())
        if number_of_dice > 1 and number_of_dice < 11:
            reply = ""
            for dice in range(number_of_dice):
                reply += self.reply_text % str(random.randrange(1, 7)) + '\n'
        elif number_of_dice == 1 or self.arguments == None:
            reply = self.reply_text % random.randrange(1, 7)
        elif number_of_dice == 0:
            reply = self.dialogs['reply_0']
        else:
            reply = self.dialogs['reply_max']
        return {'message': reply}
