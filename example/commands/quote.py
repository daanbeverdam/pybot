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
        else:
            tokens = arguments.split(' ')
            if len(tokens) > 1:
                if ':' in arguments:
                    name = arguments.split(':')[0]
                    quote = '"' + arguments.split(':')[1].strip() + '"'
                    try:
                        quotes[name].append(quote)
                        self.data['quote_store'] = quotes
                    except:
                        quotes[name] = [quote]
                        self.data['quote_store'] = quotes
                    reply = self.dialogs['quote_saved']
                elif tokens[0] in quotes and tokens[1] == 'all':
                    quote_list = []
                    for quote in quotes[tokens[0]]:
                        quote_list.append(quote)
                    reply = '\n'.join(map(str, quote_list))
            elif len(tokens) == 1:
                if tokens[0] in quotes:
                    quote_list = quotes[tokens[0]]
                    reply = random.choice(quote_list)
                if tokens[0] == 'all':
                    quote_list = []
                    for name in quotes:
                        for quote in quotes[name]:
                            quote_list.append(quote)
                    reply = '\n'.join(map(str, quote_list))
        return {'message': reply}

    def check_quote_store(self):
        try:
            quote_store = self.data['quote_store']
        except:
            self.data['quote_store'] = {}
