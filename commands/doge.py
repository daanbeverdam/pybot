import StringIO
import urllib
from core.command import Command


class DogeCommand(Command):

    def reply(self, response):
        caption = self.arguments
        image_url = ('http://dogr.io/' + '/'.join(map(str, caption.split())) +
                     '.png?split=false')
        doge_image = (StringIO.StringIO(urllib.urlopen(image_url)
                      .read()).getvalue())
        response.send_photo.photo = doge_image
        return response
