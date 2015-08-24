from command import Command
import re, urllib

class BBQCommand(Command):

	def __init__(self):
		pass

	def get_bbq_weather(self):
		url = "http://www.barbecueweer.nl"
    	grade = re.search(r'<div class="cijfer[\'"]?([^\'" >]+)', urllib.urlopen(url).read()).group(1)
    	#return reply
