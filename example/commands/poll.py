from pybot.command import Command
import shelve


class PollCommand(Command):

    def new_poll(self):
        tokens = self.arguments().split('-')
        question = tokens[0]
        self.data['poll_question'] = question
        options = []
        options_dict = {}
        for option in tokens[1:]:
            options.append([option.strip()])
            options_dict[option.strip()] = ''
        self.data['poll_options'] = options
        self.data['poll_options_dict'] = options_dict
        self.data['poll_participators'] = []
        self.data['poll_starter'] = self.message.sender_id
        self.data['poll_active'] = True
        print options,options_dict
        return {'message': question, 'keyboard': options, 'force_reply': True}

    def store_answer(self):
        if self.message.sender_id not in self.data['poll_participators']:
            participators = self.data['poll_participators']
            participators.append(self.message.first_name_sender)
            self.data['poll_options_dict'][self.message.text] += (
                                                 self.message.first_name_sender)
            return {'message': self.dialogs['store_answer'], 'keyboard': None,
                    'selective': True, 'message_id': self.message.id}
        return {'message': None}

    def handle_meta(self):
        if self.message.text == '/results':
            return self.poll_results()
        return self.end_poll()

    def poll_results(self):
        reply = self.dialogs['results']
        for option, voters in self.data['poll_options_dict']:
            reply += '\n' + key + ': ' + ', '.join(map(str, voters))
        return {'message': reply}

    def end_poll(self):
        if self.message.sender_id == self.data['poll_starter']:
            self.data['poll_active'] = False
            return {'message': self.dialogs['end_poll'], 'keyboard': None}
        return {'message': self.dialogs['not_owner']}

    def reply(self):
        if not self.is_active():
            return self.new_poll()
        elif self.message.text in self.data['poll_options_dict']:
            return self.store_answer()
        elif self.message.text in self.meta_commands:
            return self.handle_meta()
        elif self.message.text.split(' ', 1)[0][1:] == self.name:
            return {'message': self.dialogs['poll_already_active']}
        return {'message': None}
