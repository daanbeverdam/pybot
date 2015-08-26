import urllib, urllib2
import json
import StringIO
import random

class PutinCommand():

    def __init__(self, arguments):
        self.usage = {'message' : 'Het commando /putin retourneert een willekeurige foto van Putin.'}
        self.reply_type = 'message' if arguments == 'help' else 'photo'
        self.result = self.usage if arguments == 'help' else self.get_putin_photo()

    def get_putin_photo(self):
        url = "http://api.tumblr.com/v2/blog/vladimirputindoingthings.tumblr.com/posts/text?&limit=50"
        resp = urllib2.urlopen(url).read()
        content = json.loads(resp)
        post_list = content['response'].get("posts")
        random_post_body = random.choice(post_list).get('body')
        photo_url = random_post_body.split('src=')[1].split('/>')[0].strip('"')
        photo = StringIO.StringIO(urllib.urlopen(photo_url).read()).getvalue()
        return {'photo' : photo}