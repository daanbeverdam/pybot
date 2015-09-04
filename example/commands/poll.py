from pybot.command import Command
import shelve


class PollCommand(Command):

    def new_poll(self):
        tokens = self.arguments().split('*')
        question = tokens[0].strip()
        self.data['poll_question'] = question
        options = []
        options_dict = {}
        for option in tokens[1:]:
            options.append(option.strip())
            options_dict[option.strip()] = []
        formatted_options = self.format(question, options)
        self.data['poll_options_dict'] = options_dict
        self.data['poll_participators'] = []
        self.data['poll_starter'] = self.message.sender_id
        if question != '':
            self.data['poll_active'] = True
            reply = question
        return {'message': reply, 'keyboard': formatted_options,
                'force_reply': True}

    def format(self, question, options):
        formatted_options = [['"' + question + '"' ]]
        temp_options = []
        counter = 1
        for option in options:
            temp_options.append(option)
            if counter % 2 == 0:
                formatted_options.append(temp_options)
                temp_options = []
            counter +=1
        if len(temp_options) > 0:
            formatted_options.append(temp_options + [' '])
        return formatted_options

    def store_answer(self):
        participators = self.data['poll_participators']
        if self.message.sender_id not in participators:
            participators.append(self.message.sender_id)
            self.data['poll_participators'] = participators
            option_dict = self.data['poll_options_dict']
            option_dict[self.message.text].append(self.message.first_name_sender)
            self.data['poll_options_dict'] = option_dict
            return {'message': self.dialogs['store_answer'], 'keyboard': None,
                    'selective': True, 'message_id': self.message.id}
        return {'message': None}

    def handle_meta(self):
        if self.message.text == '/results':
            return self.poll_results()
        return self.end_poll()

    def poll_results(self):
        reply = self.dialogs['results'] % self.data['poll_question']
        for option, voters in self.data['poll_options_dict'].iteritems():
            reply += ('\n' + option + ': ' + ', '.join(map(str, voters)) +
                      ' (%d %s)' % (len(voters), self.dialogs[('vote'
                      if len(voters) == 1 else 'votes')]))
        return {'message': reply}

    def end_poll(self):
        if self.message.sender_id == self.data['poll_starter']:
            self.data['poll_active'] = False
            return {'message': self.dialogs['end_poll'], 'keyboard': None}
        return {'message': self.dialogs['not_owner']}

    def reply(self):
        if self.arguments() == 'help':
            return {'message': self.usage}
        elif not self.is_active():
            return self.new_poll()
        elif self.message.text in self.data['poll_options_dict']:
            return self.store_answer()
        elif self.message.text in self.meta_commands:
            return self.handle_meta()
        elif self.message.text.split(' ', 1)[0][1:] == self.name:
            return {'message': self.dialogs['poll_already_active']}
        return {'message': None}
