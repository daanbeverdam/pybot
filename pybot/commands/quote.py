from pybot.core.command import Command
from pybot.core.response import Response
from pybot.helpers.quote import QuoteHelper
import random


class QuoteCommand(Command):
    """Command that saves and returns quotes."""

    def reply(self, response):

        if not self.arguments:
            reply = self.random_quote()
            if not reply:
                reply = self.dialogs['no_quotes']

        else:
            tokens = self.arguments.split()

            if len(tokens) > 1:

                if ':' in self.arguments:
                    reply = self.save_quote()

                elif tokens[1] == 'all':
                    reply = self.all_quotes_by_name(tokens)

            elif len(tokens) == 1:

                if tokens[0] == 'all':
                    reply = self.all_quotes(tokens)

                else:
                    reply = self.random_quote_by_name(tokens)

        chunks = self.chunk(reply)
        responses = []

        for reply in chunks:
            response = Response(self.message.chat.id)
            response.send_message.text = reply
            responses.append(response)

        return responses

    def random_quote(self):
        helper = QuoteHelper()
        quote = helper.get_random_quote(self.message.chat)
        return quote

    def random_quote_by_name(self, tokens):
        quote_list = self.quotes[tokens[0].title()]
        return random.choice(quote_list) + ' -' + tokens[0].title()

    def save_quote(self):
        name = self.arguments.split(':')[0].title()
        if name == 'all':
            return self.dialogs['all_reserved']
        quote = '"' + self.arguments.split(':')[1].strip() + '"'
        helper = QuoteHelper()
        helper.save_quote(chat, name, quote)
        return self.dialogs['quote_saved']

    def all_quotes_by_name(self, tokens):
        quote_list = []
        for quote in self.quotes[tokens[0].title()]:
            quote_list.append(quote)
        return ('\n'.join(quote_list) + '\n -' +
                tokens[0].title())

    def all_quotes(self, tokens):
        helper = QuoteHelper()
        quotes = helper.get_all_quotes(self.message.chat)
        reply = ''
        for name, quote in quotes:
            reply += quote + ' -' + name + '\n'
        return reply
