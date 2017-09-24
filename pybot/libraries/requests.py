from pybot.core.message import Message
from pybot.core.response import Response
from pybot.core.user import User
from pybot.etc import config
import requests
import json
import urllib


class Requests():
    """Class that handles all bot requests."""
    def __init__(self):
        self.REQUEST_URL = 'https://api.telegram.org/bot' + config.TOKEN + '/'

    def reply(self, response):
        #TODO: move reply function from pybot to here?
        pass

    def send_action(self, chat_id, action):
        act = urllib.urlopen(self.base_url + 'sendChatAction',
                              urllib.urlencode({
                               'chat_id': str(chat_id),
                               'action': str(action)
                               })).read()
        return act

    def get_me(self):
        update_url = self.base_url + 'getMe'
        request = urllib.request.urlopen(update_url)
        update = json.loads(request.read().decode('utf-8'))
        if update['ok'] and update['result']:
            result = update['result']
            return User(id=result['id'], first_name=result['first_name'], username=result['username'])

    def get_chat_members_count(self, chat):
        """Returns no of members in a chat, accepts chat object."""
        url = self.REQUEST_URL + 'getChatMembersCount'
        parameters = {'chat_id': chat.id}
        result = requests.get(url, params=parameters)
        result = json.loads(result.text)
        if result['ok']:
            return result['result']
        return None

    def kick_chat_member(self, chat, member, until_date=None):
        """Kicks member from chat, accepts chat and user objects. Unixtimestamp is optional."""
        url = self.REQUEST_URL + 'kickChatMember'
        parameters = {
            'chat_id': chat.id,
            'user_id': member.id,
            'until_date': until_date
        }
        result = requests.get(url, params=parameters)
        result = json.loads(result.text)
        if result['ok']:
            return {
                'kicked': True,
                'text': result['result']
                }
        else:
            return {
                'kicked': False,
                'text': result['description']
                }

    def get_chat_invite_link(self, chat):
        """Returns chat invite link for chat, accepts chat object."""
        url = self.REQUEST_URL + 'exportChatInviteLink'
        parameters = {'chat_id': chat.id}
        result = requests.get(url, params=parameters)
        result = json.loads(result.text)
        if result['ok']:
            return result['result']
        return None
