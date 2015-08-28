import re, urllib

class BBQCommand():

    def __init__(self, arguments):
        self.usage = {'message': "Het commando /bbq geeft het huidige barbecueweercijfer voor Nederland."}
        self.reply_type = 'message'
        self.result =  self.usage if arguments == 'help' else self.get_bbq_weather()

    def get_bbq_weather(self):
        url = "http://www.barbecueweer.nl"
        grade = re.search(r'<div class="cijfer[\'"]?([^\'" >]+)', urllib.urlopen(url).read()).group(1)
        reply = "Het barbecueweer krijgt vandaag een " + grade + ". Oant moarn!"
        return {'message' : reply}