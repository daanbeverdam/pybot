import json
import urllib
from core.command import Command


class WikiCommand(Command):

    def reply(self, response):
        search_url = ("https://en.wikipedia.org/w/api.php?action=query&list=se"
                      "arch&srsearch=" + self.arguments + "&utf8=&format=json")
        search_results = json.loads(urllib.urlopen(search_url).read())
        if search_results['query']['searchinfo']['totalhits'] > 0:
            article_title = search_results['query']['search'][0]['title']
            article_url = ("https://en.wikipedia.org/w/api.php?format=json"
                           "&action=query&prop=extracts&exintro=&explaintext="
                           "&titles=" + article_title + "&exchars=500")
            article_contents = json.loads(urllib.urlopen(article_url).read())
            wiki_url = ('https://en.wikipedia.org/wiki/' +
                        article_title.replace(' ', '_'))
            # extract = (article_contents['query']['pages']
            #            [list(article_contents['query']['pages'])
            #            [0]]['extract'] + '\n' + wiki_url)
            # response.send_message.text = extract
            response.send_message.text = wiki_url
            return response
        response.send_message.text = self.dialogs['no_results'] % self.arguments
        return response
