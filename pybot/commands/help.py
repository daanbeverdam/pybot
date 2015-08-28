class HelpCommand():

    def __init__(self, arguments):
        self.usage = {'message': "Helpception! Try /help for a list of commands."}
        self.reply_type = 'message'
        self.result = self.get_help()

    def get_help(self):
        reply = "List of commands:"
        # for command in Command.dictionary:
        #     reply += '\n/' + command[0]
        return {'message' : reply}
