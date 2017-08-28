from pybot.core.command import Command
from pybot.helpers.poll import PollHelper


class ResultsCommand(Command):
    """Command that returns poll results."""

    def reply(self, response):
        helper = PollHelper()
        results = helper.get_results(self.message.chat)
        if results:
            question = helper.get_question(self.message.chat)
            reply = self.dialogs['reply'] % question
            for option, voters in results.items():
                reply += ('\n\u2022 ' + option + ': ' + ', '.join(voters) +
                          ' (%d %s)' % (len(voters), self.dialogs[(
                                        'vote' if len(voters) == 1 else 'votes')]))
        else:
            reply = self.dialogs['not_active']
        response.send_message.text = reply
        return response
