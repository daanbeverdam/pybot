class ExampleCommand():

    def __init__(self, arguments):
        self.usage = {'message': "Help text."}
        self.reply_type = 'message' if arguments == 'help' else 'reply_type'
        self.arguments = 'help' if arguments == None else arguments
        self.result =  self.usage if arguments == 'help' else self.get_example(self.arguments)

    def get_example(self,input):
 		# get something
 		reply = "blabla"
        return {'message' : reply}
