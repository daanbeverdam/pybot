from core.command import Command
import shelve


class PollCommand(Command):

    def reply(self, response):
        if not self.is_active():
            return self.new_poll(response)

        elif self.db_get()['allow_add'] and self.arguments and self.arguments.split()[0] == 'add':
            return self.add_poll_option(response)

        elif self.message.text in self.db_get()['options_dict']:
            return self.store_answer(response)

        elif self.message.text.split(' ', 1)[0][1:] == self.name:
            return {'message': self.dialogs['poll_already_active']}

        return None

    def new_poll(self, response, keep_old_results=False):
        one_time = True
        self.db_set('original_arguments', self.arguments)

        if self.arguments[:2] in ['~m', '~M']:
            self.db_set('multi', True)
            one_time = False

            if self.arguments[:3] in ['~ma', '~MA', '~mA', '~Ma']:
                self.db_set('allow_add', True)
                self.arguments = self.arguments[3:]

            else:
                self.db_set('allow_add', False)
                self.arguments = self.arguments[2:]

        elif self.arguments[:2] in ['~a', '~A']:
            self.db_set('allow_add', True)

            if self.arguments[:3] in ['~am', '~AM', '~aM', '~Am']:
                self.db_set('multi', True)
                one_time = False
                self.arguments = self.arguments[3:]

            else:
                self.db_set('multi', False)
                self.arguments = self.arguments[2:]

        else:
            self.db_set('multi', False)
            self.db_set('allow_add', False)
            one_time = True

        tokens = self.arguments.split('*')
        question = tokens[0].strip()
        self.db_set('question', question)
        options = []
        options_dict = {}

        for option in tokens[1:]:
            options.append(option.strip())
            options_dict[option.strip()] = []

        if not keep_old_results:
            self.db_set('options_dict', options_dict)
            self.db_set('participators', [])

        else:
            new_option = self.arguments.split('*')[-1].strip()
            poll_option_dict = self.db_get()['options_dict']
            poll_option_dict[new_option] = []
            self.db_set('options_dict', poll_option_dict)

        self.db_set('starter', self.message.sender.id)
        self.db_set('starter_name', self.message.sender.first_name)

        if question != '' and len(options_dict) > 0:
            self.activate(True)
            response.send_message.text = question + '\n- ' + '\n- '.join(options)
            response.send_message.reply_markup.keyboard = self.format(question, options)
            response.send_message.force_reply = True
            response.send_message.reply_markup.one_time_keyboard = one_time
        else:
            print 'No question or options specified!'
            raise

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

        if self.db_get()['multi']:
            temp_options.append('/done')

        if len(temp_options) == 1:
            formatted_options.append(temp_options + [' '])

        elif len(temp_options) == 2:
            formatted_options.append(temp_options)

        return formatted_options

    def store_answer(self, response):
        participators = self.db_get()['participators']

        if (self.message.sender.id not in participators or self.db_get()['multi'] and
                self.message.sender.first_name not in self.db_get()['options_dict'][self.message.text]):
            participators.append(self.message.sender.id)
            self.db_set('participators', participators)
            option_dict = self.db_get()['options_dict']
            option_dict[self.message.text].append(self.message.sender.first_name)
            self.db_set('options_dict', option_dict)

            if self.db_get()['multi']:
                response.send_message.text = self.dialogs['store_answer']

            else:
                response.send_message.text = self.dialogs['store_answer']
                response.send_message.reply_markup.hide_keyboard = True
                response.send_message.reply_markup.selective = True

            chat_users = self.db.chats.find_one({'id': self.message.chat.id})['users']

            if len(participators) == len(chat_users) and not self.db_get()['multi']:
                response.send_message.text = self.dialogs['everybody_voted'] % self.poll_results()
                response.send_message.reply_markup.hide_keyboard = True
                response.send_message.reply_markup.selective = False
                self.activate(False)

            return response

        return None

    def add_poll_option(self, response):
        self.arguments = self.db_get()['original_arguments'] + '*' + self.arguments[3:]
        return self.new_poll(response, keep_old_results=True)

    def cancel(self, response):
        if self.message.sender.id == self.db_get()['starter'] or self.message.sender.id == self.admin:
            self.activate(False)
            response.send_message.text = self.dialogs['end_poll']
            response.send_message.reply_markup.hide_keyboard = True
            return response
        response.send_message.text = self.dialogs['not_owner'] % self.db_get()['starter_name']

    def done(self, response):
        response.send_message.text = self.dialogs['done_voting']
        response.send_message.reply_markup.hide_keyboard = True
        response.send_message.reply_markup.selective = True
        return response

    def poll_results(self):
        reply = self.dialogs['results'] % self.db_get()['question']
        for option, voters in self.db_get()['options_dict'].iteritems():
            reply += ('\n- ' + option + ': ' + ', '.join(voters) +
                      ' (%d %s)' % (len(voters), self.dialogs[(
                                    'vote' if len(voters) == 1 else 'votes')]))
        return reply
