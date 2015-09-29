from pybot.command import Command
import json
import urllib


class XKCDCommand(Command):

    def reply(self):
        url = 'http://xkcd.com/info.0.json'
        content = json.loads(urllib.urlopen(url).read())
        image_link = content['img']
        xkcd_photo = self.get_image(image_link)
        return {'photo': xkcd_photo}
