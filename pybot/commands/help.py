class HelpCommand():

    def __init__(self, arguments):
        self.usage = {'message': "Helpception error! Probeer /help voor een lijst met commando's."}
        self.reply_type = 'message'
        self.result = self.get_help()

    def get_help(self):
        reply = "Lijst met commando's:"
        # for command in Command.dictionary:
        #     reply += '\n/' + command[0]
        #
        return {'message' : reply}
