import random

class DiceCommand():

    def __init__(self, arguments):
        self.usage = {'message': "Gooi een dobbelsteen met /dice. Gooi meerdere stenen door "
            "een getal toe te voegen, bijvoorbeeld: /dice 2."}
        self.reply_type = 'message'
        self.arguments = 1 if arguments == None else arguments
        self.result =  self.usage if arguments == 'help' else self.throw_dice(int(self.arguments))

    def throw_dice(self, number_of_dice):
        reply = ""
        if number_of_dice > 1 and number_of_dice < 11:
            for dice in range(number_of_dice):
                reply += str(dice+1) + 'e dobbelsteen: ' + str(random.randrange(1,7)) + '\n'
        elif number_of_dice == 1:
            reply += "Je gooide: %i" % random.randrange(1,7)
        else:
            reply += "Het maximum aantal dobbelstenen dat je kan gooien is 10. Kies een lager getal."
        return {'message' : reply}
