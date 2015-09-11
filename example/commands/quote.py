from pybot.command import Command
import random
import shelve


class QuoteCommand(Command):

    def reply(self):
        arguments = self.arguments()
        self.check_quote_store()
        if arguments == None:
            reply = self.random_quote()
        else:
            tokens = arguments.split(' ')
            if len(tokens) > 1:
                if ':' in arguments:
                    reply = self.save_quote()
                elif tokens[0].title() in self.data['quote_store'] and tokens[1] == 'all':
                    reply = self.all_quotes_by_name(tokens)
            elif len(tokens) == 1:
                if tokens[0].title() in self.data['quote_store']:
                    reply = self.random_quote_by_name(tokens)
                if tokens[0] == 'all':
                    reply = self.all_quotes(tokens)
        return {'message': reply}

    def random_quote(self):
        random_name = random.choice(self.data['quote_store'].keys())
        quote_list = self.data['quote_store'][random_name]
        return random.choice(quote_list) + ' -' + random_name

    def random_quote_by_name(self, tokens):
        quote_list = self.data['quote_store'][tokens[0].title()]
        return random.choice(quote_list) + ' -' + tokens[0].title()

    def save_quote(self):
        name = self.arguments().split(':')[0].title()
        quote = '"' + self.arguments().split(':')[1].strip() + '"'
        quotes = self.data['quote_store']
        try:
            quotes[name].append(quote)
            self.data['quote_store'] = quotes
        except:
            quotes[name] = [quote]
            self.data['quote_store'] = quotes
        return self.dialogs['quote_saved']

    def all_quotes_by_name(self, tokens):
        quote_list = []
        for quote in self.data['quote_store'][tokens[0].title()]:
            quote_list.append(quote)
        return ('\n'.join(map(str, quote_list))  + '\n -' +
                tokens[0].title())

    def all_quotes(self, tokens):
        quote_list = []
        for name in self.data['quote_store']:
            for quote in self.data['quote_store'][name]:
                quote_list.append(quote + ' -' + name)
        return '\n'.join(map(str, quote_list))

    def check_quote_store(self):
        try:
            quote_store = self.data['quote_store']
        except:
            self.data['quote_store'] = {}
