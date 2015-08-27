import StringIO
import urllib

class DogeCommand():

    def __init__(self, arguments):
        self.usage = {'message': "Maak je eigen doge afbeelding met caption. "
            "Stuur bijvoorbeeld '/doge wow such doge'."}
        self.reply_type = 'message' if arguments == 'help' else 'photo'
        self.arguments = 'wait for user input' if arguments == None else arguments
        self.result =  self.usage if arguments == 'help' else self.get_doge_photo(self.arguments)

    def get_doge_photo(self, caption):
        photo_url = 'http://dogr.io/' + '/'.join(map(str,caption.split())) + '.png?split=false'
        photo = StringIO.StringIO(urllib.urlopen(photo_url).read()).getvalue()
        return {'photo' : photo}