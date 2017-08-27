from pybot.core.command import Command
import shelve
from pybot.helpers.poll import PollHelper


class PollCommand(Command):

    def reply(self, response):

        if not self.message.text:
            return None

        elif not self.is_active():
            return self.new_poll(response)

        elif self.message.text in PollHelper().get_options(self.message.chat):
            return self.store_answer(response)

        elif self.message.text.split(' ', 1)[0] == self.name:
            response.send_message.text = self.dialogs['poll_already_active']
            return response

    def new_poll(self, response):
        # TODO: parse command flags
        helper = PollHelper()
        tokens = self.arguments.split('*')
        question = tokens[0].strip()
        options = [token.strip() for token in tokens[1:]]

        if question != '' and len(options) > 0:
            helper.store_question(question, self.message.sender, self.message.chat)
            helper.store_options(options, self.message.chat)
            self.activate(True)
            response.send_message.text = question + '\n- ' + '\n- '.join(options)
            response.send_message.reply_markup.keyboard = self.format(question, options)
            response.send_message.force_reply = True
            response.send_message.reply_markup.one_time_keyboard = True
        else:
            raise ValueError('No question or options specified!')
        return response

    def format(self, question, options):
        formatted_options = [['"%s"' % question]]
        temp_options = []
        counter = 1

        for option in options:
            temp_options.append(option.strip())
            if counter % 2 == 0:
                formatted_options.append(temp_options)
                temp_options = []
            counter += 1

        if len(temp_options) == 1:
            formatted_options.append(temp_options + [' '])

        elif len(temp_options) == 2:
            formatted_options.append(temp_options)

        return formatted_options

    def store_answer(self, response):
        helper = PollHelper()
        helper.register_option(self.message.text, self.message.sender, self.message.chat)
        response.send_message.text = self.dialogs['store_answer']
        response.send_message.reply_markup.hide_keyboard = True
        response.send_message.reply_markup.selective = True
        response.send_message.reply_to_message_id = self.message.id
        return response

    def add_poll_option(self, response):
        self.arguments = self.db_get()['original_arguments'] + '*' + self.arguments[3:]
        return self.new_poll(response, keep_old_results=True)

    def cancel(self, response):
        helper = PollHelper()
        initiator = helper.get_initiator(self.message.chat)
        if self.message.sender.id == initiator.id or self.message.sender.id == self.admin:
            self.activate(False)
            response.send_message.text = self.dialogs['end_poll']
            response.send_message.reply_markup.hide_keyboard = True
            return response
        response.send_message.text = self.dialogs['not_owner'] % helper.get_initiator().first_name
        return response

    def done(self, response):
        response.send_message.text = self.dialogs['done_voting']
        response.send_message.reply_markup.hide_keyboard = True
        response.send_message.reply_markup.selective = True
        response.send_message.reply_to_message_id = self.message.id
        return response

    def poll_results(self):
        reply = self.dialogs['results'] % self.db_get()['question']
        for option, voters in self.db_get()['options_dict'].iteritems():
            reply += ('\n- ' + option + ': ' + ', '.join(voters) +
                      ' (%d %s)' % (len(voters), self.dialogs[(
                                    'vote' if len(voters) == 1 else 'votes')]))
        return reply
