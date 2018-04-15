import time
from pybot.core.command import Command
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

            if self.is_stale():
                PollHelper().delete_poll(self.message.chat)
                return self.new_poll(response)

            else:
                response.send_message.text = self.dialogs['poll_already_active']

            return response

    def new_poll(self, response):
        # TODO: parse command flags
        helper = PollHelper()
        tokens = self.arguments.split('*')
        question = tokens[0].strip()
        options = [token.strip() for token in tokens[1:]]

        if len(options) != len(set(options)):
            response.send_message.text = self.dialogs['duplicate_options']
            return response

        if question != '' and len(options) > 0:
            timestamp = int(time.time())
            helper.store_question(question, self.message.sender, self.message.chat, timestamp)
            helper.store_options(options, self.message.chat)
            self.activate(True)
            response.send_message.text = question + ' \U0001F4CA\n\u2022 ' + '\n\u2022 '.join(options)
            response.send_message.reply_markup.keyboard = self.format(question, options)
            response.send_message.force_reply = True
            response.send_message.reply_markup.one_time_keyboard = True

        else:
            raise ValueError('No question or options specified!')

        return response

    def format(self, question, options):
        formatted_options = [['%s \U0001F4CA' % question]]
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
        if not helper.has_voted(self.message.sender, self.message.chat):
            helper.register_option(self.message.text, self.message.sender, self.message.chat)
            response.send_message.text = self.dialogs['store_answer']
            response.send_message.reply_markup.hide_keyboard = True
            response.send_message.reply_markup.selective = True
            response.send_message.reply_to_message_id = self.message.id
            return response
        return None

    def cancel(self, response):
        helper = PollHelper()
        initiator = helper.get_initiator(self.message.chat)
        if self.message.sender.id in [initiator.id, self.admin]:
            helper.delete_poll(self.message.chat)
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

    def is_stale(self):
        current_timestamp = int(time.time())
        stale_period = 24 * 60 * 60  # one day
        helper = PollHelper()
        initiation_timestamp = helper.get_initiated_at(self.message.chat)

        print (initiation_timestamp)

        if current_timestamp - initiation_timestamp > stale_period:
            return True

        return False
