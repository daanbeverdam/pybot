import re, urllib

class BBQCommand(object):

    def __init__(self):
        self.usage = ""

    def get_bbq_weather(self):
        url = "http://www.barbecueweer.nl"
        grade = re.search(r'<div class="cijfer[\'"]?([^\'" >]+)', urllib.urlopen(url).read()).group(1)
        #return reply
        pass
