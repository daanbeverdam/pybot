import urllib
import json
from pybot.core.command import Command


class ChangesCommand(Command):
    """Facilitates the /changes command. Returns latest release info."""

    def reply(self, response):
        url = "https://api.github.com/repos/daanbeverdam/pybot/releases/latest"
        release = json.load(urllib.request.urlopen(url))
        reply = "\n<strong>%s</strong>\n\n%s" % (release['name'], release['body'])
        reply += '\n' + self.dialogs['more']
        response.send_message.text = reply
        response.send_message.disable_web_page_preview = True
        response.send_message.parse_mode = "HTML"
        return response
