from pybot.core.command import Command
from xml.dom.minidom import parse
import urllib


class ChangesCommand(Command):

    def reply(self, response):
        feed = 'https://github.com/daanbeverdam/pybot/commits/master.atom'
        xml = parse(urllib.request.urlopen(feed))
        reply = self.dialogs['reply']
        for node in xml.getElementsByTagName('title')[1:6]:
            reply += u'\n- ' + node.firstChild.nodeValue.strip()
        reply += u'\n' + self.dialogs['more']
        response.send_message.text = reply
        response.send_message.disable_web_page_preview = True
        return response
