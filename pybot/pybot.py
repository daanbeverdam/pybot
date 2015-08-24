import commands.putin

class PyBot(object):
    commands = {
        'putin': commands.putin.PutinCommand
    }

    def __init__(self, name, api_key):
        self.name = name
        self.api_key = api_key

    def run(self):
        while True:
            self.check_for_updates()

    def check_for_updates(self):
        response = get_updates()

        if response['ok']:
            pass
        else:
            log_message('Invalid reponse')
