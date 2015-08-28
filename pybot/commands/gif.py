import json
import StringIO
import urllib

class GifCommand():

    def __init__(self, arguments):
        self.usage = {'message': "Search for gifs using /gif [search query]. " 
        "You can ask for a random gif using '/gif random [optional search query]'."}
        self.reply_type = 'message' if arguments == 'help' else 'gif'
        self.arguments = 'help' if arguments == None else arguments
        self.result =  self.usage if self.arguments == 'help' else self.get_gif(self.arguments)

    def get_gif(self, query):
        if query.lower() == 'random':
            url = 'http://api.giphy.com/v1/gifs/random?api_key=dc6zaTOxFJmzC'
            search_response = urllib.urlopen(url)
            search_results = search_response.read()
            results = json.loads(search_results)
            gif_url = results['data']['image_original_url']
        elif query.lower().startswith('random'):
            query = query.split(' ',1)[1]
            url = 'http://api.giphy.com/v1/gifs/random?api_key=dc6zaTOxFJmzC&tag=' + '+'.join(map(str,query.split()))
            search_response = urllib.urlopen(url)
            search_results = search_response.read()
            results = json.loads(search_results)
            gif_url = results['data']['image_original_url']
        else:
            url = 'http://api.giphy.com/v1/gifs/search?q=' + '+'.join(map(str,query.split())) + '&api_key=dc6zaTOxFJmzC'
            search_response = urllib.urlopen(url)
            search_results = search_response.read()
            results = json.loads(search_results)
            gif_url = results['data'][0]['images']['original']['url']
        gif = StringIO.StringIO(urllib.urlopen(gif_url).read()).getvalue()
        return {'gif' : gif}