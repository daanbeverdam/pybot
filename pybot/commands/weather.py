from pybot.core.command import Command
import json
import urllib


class WeatherCommand(Command):
    """Returns the actual weather to the user."""

    def reply(self, response):
        query = self.arguments
        url = ('http://api.openweathermap.org/data/2.5/weather?q=' + query +
               '&units=metric&lang=' + self.dialogs['lang'] + '&appid=' +
               self.api_key)
        results = json.loads(urllib.request.urlopen(url).read())

        try:
            place = str(results['name'])
            temp = str(results['main']['temp'])
            description = str(results['weather'][0]['description'])
            reply = self.dialogs['reply'] % (temp, place, description)

        except:
            reply = self.dialogs['error'] % query

        response.send_message.text = reply
        return response
