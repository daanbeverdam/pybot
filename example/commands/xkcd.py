from pybot.command import Command
import json
import urllib
import random


class XKCDCommand(Command):

    def reply(self):
        url = 'http://xkcd.com/info.0.json'
        content = json.loads(urllib.urlopen(url).read())
        if self.arguments == 'random' or self.arguments == 'r':
            total_comics = content['num']
            n = str(random.choice(range(1, total_comics)))
            url = 'http://dynamic.xkcd.com/api-0/jsonp/comic/' + n
            content = json.loads(urllib.urlopen(url).read())
            image_link = content['img']
        else:
            image_link = content['img']
        title = '"%s"' % content['title']
        xkcd_image = self.get_image(image_link)
        return {'photo': xkcd_image, 'caption': title}
