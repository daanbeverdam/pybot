import json
import StringIO
import urllib
from core.command import Command


class GifCommand(Command):
    """Command that returns giphy gifs to the user."""

    def reply(self, response):
        arguments = self.arguments

        if arguments.startswith('random'):

            if arguments == 'random':
                url = ('http://api.giphy.com/v1/gifs/random?'
                       'api_key=dc6zaTOxFJmzC')
            else:
                query = arguments.split(' ', 1)[1]
                url = ('http://api.giphy.com/v1/gifs/random?api_key'
                       '=dc6zaTOxFJmzC&tag=' + '+'.join(map(str,
                                                            query.split())))

        else:
            url = ('http://api.giphy.com/v1/gifs/search?q=' +
                   '+'.join(map(str, arguments.split())) +
                   '&api_key=dc6zaTOxFJmzC')

        search_response = urllib.urlopen(url)
        search_results = search_response.read()
        results = json.loads(search_results)

        if results['data'] != []:
            if 'random' in arguments:
                gif_url = results['data']['image_original_url']
            else:
                gif_url = results['data'][0]['images']['original']['url']
        else:
            response.send_message.text = self.dialogs['no_results'] % arguments
            return response

        gif = self.to_string(gif_url)
        response.send_document.document = gif
        response.send_document.name = 'giphy.gif'
        return response
