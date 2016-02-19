from core.command import Command


class StatsCommand(Command):
    """Command that returns the statistics of the current chat."""

    def reply(self, response):
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

        for user_id in sorted(user_stats, key=user_stats.get, reverse=True):
            msgs = user_stats[user_id]['total_messages']
            wrds = user_stats[user_id]['total_words']
            name = users[user_id]['first_name']
            avg = float(wrds) / msgs
            most_active_users += u"%i. %s: %i/%i/%.1f\n" % (c, name, msgs, wrds, avg)
            c += 1

        c = 1

        for command in sorted(command_stats, key=command_stats.get, reverse=True):
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
