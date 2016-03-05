from core.command import Command


class ResultsCommand(Command):
    """Command that returns poll results."""

    def reply(self, response):
        query = {'id': self.message.chat.id}
        result = self.db.chats.find_one(query)['commands']['/poll']
        reply = self.dialogs['reply'] % result['question']

        for option, voters in result['options_dict'].iteritems():
            reply += ('\n- ' + option + ': ' + ', '.join(voters) +
                      ' (%d %s)' % (len(voters), self.dialogs[(
                                    'vote' if len(voters) == 1 else 'votes')]))

        if result['active'] is False:
            reply += '\n' + self.dialogs['not_active']

        response.send_message.text = reply
        return response
