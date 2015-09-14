from pybot.command import Command


class CalculatorCommand(Command):

    def reply(self):
        if self.is_active():
            return self.collect_input()
        else:
            return self.start_calculator()

    def start_calculator(self):
        prompt = 'Je som?'
        calculator = ([['1','2','3','+'], ['4','5','6','-'],
                      ['7','8','9','*'], ['0','.','=','/']])
        self.data['calc_starter'] = self.message.sender_id
        self.data['calc_query'] = ''
        self.data['calculator_active'] = True
        return {'message': prompt, 'keyboard': calculator, 'one_time': False,
               'selective': True, 'force_reply': True}

    def collect_input(self):
        operators = ['*', '/', '.', '+', '-']
        if self.message.sender_id == self.data['calc_starter']:
            if self.message.text.isdigit() or self.message.text in operators:
                query = self.data['calc_query']
                query += self.message.text
                self.data['calc_query'] = query
                print 'collect'
                return {'message': None}
            elif self.message.text == '=':
                answer = "%i" % eval(self.data['calc_query'])
                print 'answer incoming'
                self.data['calculator_active'] = False
                return {'message': answer, 'keyboard': None}
        return {'message': None}

