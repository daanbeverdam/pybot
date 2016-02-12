from core.command import Command
from core.response import Response


class EchoCommand(Command):

    def reply(self):
        # self.response.send_message.text = self.arguments
        self.response.send_photo.photo = self.get_image('http://www.keenthemes.com/preview/metronic/theme/assets/global/plugins/jcrop/demos/demo_files/image1.jpg')
        self.response.send_photo.name = 'name.png'
        self.response.send_photo.caption = 'this is a photo'
        self.response.send_photo.reply_markup.keyboard = [['a'],['b']]
        return self.response
