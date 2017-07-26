from pybot.core.command import Command
from pybot.core.response import Response
import random


class QuoteCommand(Command):
    """Command that saves and returns quotes."""

    def reply(self, response):
        self.check_quotes()

        if not self.arguments and self.quotes == {}:
            reply = self.dialogs['no_quotes']

        elif not self.arguments:
            reply = self.random_quote()

        else:
            tokens = self.arguments.split()

            if len(tokens) > 1:

                if ':' in self.arguments:
                    reply = self.save_quote()

                elif tokens[0].title() in self.quotes and tokens[1] == 'all':
                    reply = self.all_quotes_by_name(tokens)

            elif len(tokens) == 1:

                if tokens[0].title() in self.quotes:
                    reply = self.random_quote_by_name(tokens)

                elif tokens[0] == 'all':
                    reply = self.all_quotes(tokens)

        chunks = self.chunk(reply)
        responses = []

        for reply in chunks:
            response = Response(self.message.chat.id)
            response.send_message.text = reply
            responses.append(response)

        return responses

    def random_quote(self):
        all_quotes = []
        for quote_list in self.quotes.values():
            for quote in quote_list:
                all_quotes.append(quote)

        random_quote = random.choice(all_quotes)
        for name, quotes in self.quotes.items():
            if random_quote in quotes:
                return random_quote + ' -' + name

    def random_quote_by_name(self, tokens):
        quote_list = self.quotes[tokens[0].title()]
        return random.choice(quote_list) + ' -' + tokens[0].title()

    def save_quote(self):
        name = self.arguments.split(':')[0].title()
        if name == 'all':
            return self.dialogs['all_reserved']
        quote = '"' + self.arguments.split(':')[1].strip() + '"'
        query = {'id': self.message.chat.id}
        update = {'$push': {'commands./quote.quotes.' + name: quote}}
        self.db.chats.update(query, update, upsert=True)
        return self.dialogs['quote_saved']

    def all_quotes_by_name(self, tokens):
        quote_list = []
        for quote in self.quotes[tokens[0].title()]:
            quote_list.append(quote)
        return ('\n'.join(quote_list) + '\n -' +
                tokens[0].title())

    def all_quotes(self, tokens):
        quote_list = []
        for name in self.quotes:
            for quote in self.quotes[name]:
                quote_list.append(quote + ' -' + name)
        return '\n'.join(quote_list)

    def check_quotes(self):
        query = {'id': self.message.chat.id, 'commands./quote.quotes': {'$exists': True}}
        result = self.db.chats.find_one(query)
        if not result:
            self.db_set('quotes', {})
        self.quotes = self.db_get()['quotes']

