import random
from core.command import Command


class DiceCommand(Command):

    def reply(self, response):
        if not self.arguments:
            number_of_dice = 1
        else:
            number_of_dice = int(self.arguments)
        if number_of_dice > 1 and number_of_dice < 11:
            reply = ""
            for dice in range(number_of_dice):
                reply += self.dialogs['reply'] % random.randrange(1, 7) + '\n'
        elif number_of_dice == 1 or self.arguments is None:
            reply = self.dialogs['reply'] % random.randrange(1, 7)
        elif number_of_dice == 0:
            reply = self.dialogs['reply_0']
        else:
            reply = self.dialogs['reply_max']
        response.send_message.text = reply
        return response
