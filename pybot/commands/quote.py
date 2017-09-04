from pybot.core.command import Command
from pybot.core.response import Response
from pybot.helpers.quote import QuoteHelper
import random


class QuoteCommand(Command):
    """Command that saves and returns quotes."""

    def reply(self, response):

        if not self.arguments and self.message.reply_to_message:
            name = self.message.reply_to_message.sender.first_name
            quote = '"' + self.message.reply_to_message.text + '"'
            reply = self.save_quote(name, quote)
        elif not self.arguments:
            reply = self.random_quote()
        else:
            tokens = self.arguments.split()
            if len(tokens) > 1:
                if ':' in self.arguments:
                    reply = self.parse_quote(self.arguments)
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
        if quote:
            return quote[1] + ' -' + quote[0]
        else:
            return self.dialogs['no_quotes']

    def random_quote_by_name(self, tokens):
        helper = QuoteHelper()
        quote = helper.get_random_quote_by_name(self.message.chat, tokens[0].title())
        if quote:
            return quote[1] + ' -' + quote[0].title()
        else:
            return self.dialogs['no_quotes_for_user'] % tokens[0]

    def parse_quote(self, text):
        name = text.split(':')[0].title()
        if name == 'All':
            return self.dialogs['all_reserved']
        quote = '"' + text.split(':')[1].strip() + '"'
        return self.save_quote(name, quote)

    def save_quote(self, name, quote):
        helper = QuoteHelper()
        helper.save_quote(self.message.chat, name.strip(), quote.strip())
        return self.dialogs['quote_saved']

    def all_quotes_by_name(self, tokens):
        name = tokens[0].title()
        helper = QuoteHelper()
        quotes = helper.get_all_quotes_by_name(self.message.chat, name)
        if quotes:
            quote_list = []
            for name, quote in quotes:
                quote_list.append(quote)
            return ('\n'.join(quote_list) + '\n -' +
                    tokens[0].title())
        else:
            return self.dialogs['no_quotes_for_user'] % tokens[0]

    def all_quotes(self, tokens):
        helper = QuoteHelper()
        quotes = helper.get_all_quotes(self.message.chat)
        reply = ''
        for name, quote in quotes:
            reply += quote + ' -' + name + '\n'
        if not reply:
            return self.dialogs['no_quotes']
        return reply
