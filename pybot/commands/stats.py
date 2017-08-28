from pybot.core.command import Command
from pybot.helpers.stats import StatsHelper


class StatsCommand(Command):
    """Command that returns the statistics of the current chat."""

    def reply(self, response):
        self.collect(self.message)
        if self.message.text and self.message.text.split()[0] == self.name:
            return self.get_stats_overview()

    def get_stats_overview(self):
        query = {
            'id': self.message.chat.id
        }
        chat = self.db.chats.find_one(query)
        stats = chat['statistics']
        users = chat['users']
        user_stats = stats['users']
        command_stats = stats['commands']
        most_active_users = u""
        most_used_commands = u""
        c = 1

        for user_id in sorted(user_stats, key=lambda i: user_stats[i]['total_messages'], reverse=True):
            msgs = user_stats[user_id]['total_messages']
            wrds = user_stats[user_id]['total_words']
            name = users[user_id]['first_name']
            avg = float(wrds) / msgs
            most_active_users += u"%i. %s: %i/%i/%.1f\n" % (c, name, msgs, wrds, avg)
            c += 1

        c = 1

        for command in sorted(command_stats, key=command_stats.get, reverse=True)[:5]:
            count = command_stats[command]
            most_used_commands += u"%i. %s: %i\n" % (c, command, count)
            c += 1

        formatting = (stats['total_messages'],
                      stats['total_words'],
                      stats['total_photos'],
                      stats['total_stickers'],
                      most_used_commands,
                      most_active_users)
        reply = self.dialogs['reply'] % formatting
        response.send_message.text = reply
        return response

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
        helper.collect(self.message.chat, self.message.sender, words, sticker, photo)

        # query = {
        #     'id': message.chat.id
        # }
        # update = {
        #     '$inc': {
        #         'statistics.total_messages': 1,
        #         'statistics.total_words': words,
        #         'statistics.total_stickers': sticker,
        #         'statistics.total_photos': photo,
        #         'statistics.total_documents': document,
        #         'statistics.users.' + str(user['id']) + '.total_messages': 1,
        #         'statistics.users.' + str(user['id']) + '.total_words': words,
        #         'statistics.users.' + str(user['id']) + '.total_stickers': sticker,
        #         'statistics.users.' + str(user['id']) + '.total_photos': photo,
        #         'statistics.users.' + str(user['id']) + '.total_documents': document
        #     },
        #     '$set': {
        #         'users.' + str(user['id']): user,
        #         'title': message.chat.title,
        #         'type': message.chat.type
        #     }
        # }

        # if command:
        #     update['$inc']['statistics.commands.' + command] = 1
        #     update['$inc']['statistics.users.' + str(user['id']) + '.commands.' + command] = 1
        # self.db.chats.update(query, update, upsert=True)
