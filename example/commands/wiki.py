import json
import urllib
from pybot.command import Command


class WikiCommand(Command):

    def reply(self):
        if self.arguments() == 'help':
            return {'message': self.usage}
        query = self.arguments()
        search_url = ("https://en.wikipedia.org/w/api.php?action=query"
                      "&list=search&srsearch=" + query + "&utf8=&format=json")
        search_results = json.loads(urllib.urlopen(search_url).read())
        if search_results['query']['searchinfo']['totalhits'] > 0:
            article_title = search_results['query']['search'][0]['title']
            article_url = ("https://en.wikipedia.org/w/api.php?format=json"
                           "&action=query&prop=extracts&exintro=&explaintext="
                           "&titles=" + article_title + "&exchars=500")
            article_contents = json.loads(urllib.urlopen(article_url).read())
            extract = (article_contents['query']['pages']
                       [list(article_contents['query']['pages'])
                       [0]]['extract'])
            return {'message': extract}
        return {'message': self.dialogs['no_results'] % query}
