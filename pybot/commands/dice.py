import random

class DiceCommand():

    def __init__(self, arguments):
        self.usage = {'message': "Throw a die with /dice. Throw multiple dice by "
            "adding a number. For example: /dice 2."}
        self.reply_type = 'message'
        self.arguments = 1 if arguments == None else arguments
        self.result =  self.usage if arguments == 'help' else self.throw_dice(int(self.arguments))

    def throw_dice(self, number_of_dice):
        reply = ""
        if number_of_dice > 1 and number_of_dice < 11:
            for dice in range(number_of_dice):
                reply += "Die number " + str(dice+1) + ': ' + str(random.randrange(1,7)) + '\n'
        elif number_of_dice == 1:
            reply += "You threw: %i" % random.randrange(1,7)
        else:
            reply += "Sorry, the maximum number of dice you can throw at once is 10."
        return {'message' : reply}
