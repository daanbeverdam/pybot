from pybot.command import Command
import random
import shelve


class QuoteCommand(Command):

    def reply(self):
        arguments = self.arguments()
        self.check_quote_store()
        quotes = self.data['quote_store']
        if arguments == None:
            quote_list = quotes[(random.choice(quotes.keys()))]
            reply = random.choice(quote_list)
        elif arguments.split(' ')[0] == 'all' or arguments.split(' ')[1] == 'all':
            quote_list = []
            if arguments.split(' ') == 1:
                for name in quotes:
                    for quote in quotes[name]:
                        quote_list.append(quote)
            else:
                name = arguments.split(' ')[0]
                for quote in quotes[name]:
                    quote_list.append(quote)
            reply = '\n'.join(map(str, quote_list))
        elif arguments in quotes.keys():
            quote_list = quotes[arguments]
            reply = random.choice(quote_list)
        else:
            name = arguments.split(':')[0]
            quote = arguments.split(':')[1]
            try:
                quotes[name].append(quote)
                self.data['quote_store'] = quotes
            except:
                quotes[name] = [quote]
                self.data['quote_store'] = quotes
            reply = self.dialogs['quote_saved']
        return {'message': reply}

    def check_quote_store(self):
        try:
            quote_store = self.data['quote_store']
        except:
            self.data['quote_store'] = {}
