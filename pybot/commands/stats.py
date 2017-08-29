from pybot.core.command import Command
from pybot.helpers.stats import StatsHelper


class StatsCommand(Command):
    """Command that returns the statistics of the current chat."""

    def reply(self, response):
        self.collect(self.message)
        if self.message.text and self.message.text.split()[0] == self.name:
            reply = self.get_stats_overview()
            response.send_message.text = reply
            return response

    def get_stats_overview(self):
        helper = StatsHelper()
        overview = helper.get_overview(self.message.chat)
        most_active_users = ""
        c = 1
        sorted_users = sorted(overview, key=lambda i: overview[i][0], reverse=True)
        for name in [name for name in sorted_users if name != 'total']:
            msgs = overview[name][0]
            wrds = overview[name][1]
            avg = float(wrds) / msgs
            most_active_users += u"%i. %s: %i/%i/%.1f\n" % (c, name, msgs, wrds, avg)
            c += 1
        formatting = (overview['total'][0],
                      overview['total'][1],
                      overview['total'][2],
                      overview['total'][3],
                      most_active_users)
        reply = self.dialogs['reply'] % formatting
        return reply

    def collect(self, message):
        """Stores statistics and user information in database."""
        helper = StatsHelper()
        words = 0
        sticker = 0
        photo = 0
        if message.text:
            tokens = message.text.split()
            words = len(tokens)
        elif message.sticker:
            sticker = 1
        elif message.photo:
            photo = 1
        helper.collect(message.chat, message.sender, words, sticker, photo)
