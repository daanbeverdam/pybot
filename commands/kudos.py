from core.command import Command
import operator


class KudosCommand(Command):

    def reply(self, response):
        if self.message.text:

            if self.message.text.split()[0].split('@')[0] == self.name:

                if not self.arguments:
                    return self.kudos_overview(response)

                elif self.arguments.title() in [i['first_name'] for i in self.get_chat_users().values()]:
                    return self.give_kudos(response, self.arguments)

                response.send_message.text = self.dialogs['not_in_chat'] % self.arguments
                return response

            elif self.message.text[:2] == '+1':
                return self.give_kudos(response)

            elif self.message.text[:2] == '-1':
                return self.give_kudos(response, substract=True)

    def kudos_overview(self, response):
        result = self.db.chats.find_one({'id': self.message.chat.id, 'commands./kudos.overview': {'$exists': True}})

        if result:
            overview = self.db_get()['overview']
            reply = self.dialogs['kudo_overview']
            overview = sorted(overview.items(), key=operator.itemgetter(1), reverse=True)

            for entry in overview:
                reply += "\n%s: %i" % (entry[0], entry[1])

            response.send_message.text = reply

        else:
            response.send_message.text = self.dialogs['no_kudos']

        return response

    def give_kudos(self, response, name=None, substract=False):
        result = self.db.chats.find_one({'id': self.message.chat.id, 'commands./kudos.overview': {'$exists': True}})

        if not result:
            self.db_set('overview', {})

        if substract:
            number_of_kudos = -1

        else:
            number_of_kudos = 1

        if not name:

            try:
                name = self.message.reply_to_message.sender.first_name

            except:
                return None

        name = name.title()

        if self.message.sender.first_name == name:
            response.send_message.text = self.dialogs['shame_on_you']
            return response

        query = {
            'id': self.message.chat.id
        }
        update = {
            '$inc': {
                'commands./kudos.overview.' + name: number_of_kudos
            }
        }
        self.db.chats.update(query, update, upsert=True)
        response.send_message.text = self.dialogs['kudos_given'] % (number_of_kudos, name, self.db_get()['overview'][name])
        return response
