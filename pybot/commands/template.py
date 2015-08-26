class ExampleCommand():

    def __init__(self, arguments):
        self.usage = {'message': "Help tekst."}
        self.reply_type = 'message' if arguments == 'help' else 'reply_type'
        self.result =  self.usage if arguments == 'help' else self.get_example()

    def get_example(self):
 		# get something
        return {'message' : reply}
