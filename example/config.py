from commands.putin import PutinCommand
from commands.bbq import BBQCommand
from commands.dice import DiceCommand
from commands.doge import DogeCommand
from commands.gif import GifCommand
from commands.echo import EchoCommand
from commands.wiki import WikiCommand
from commands.youtube import YouTubeCommand
from commands.google import GoogleCommand
from commands.poll import PollCommand
from commands.help import HelpCommand
from commands.status import StatusCommand
from commands.weather import WeatherCommand
from commands.quote import QuoteCommand
import dialogs

TOKEN = '' #  enter authorization token here
BOT_NAME = 'PyBot' #  enter name of the bot here
LANG = 'en' #  'en' for english, 'nl' for dutch
COMMAND_LIST = [ #  commands can be removed or added
                BBQCommand('bbq', dialogs.bbq[LANG]),
                DiceCommand('dice', dialogs.dice[LANG]),
                DogeCommand('doge', dialogs.doge[LANG]),
                EchoCommand('echo', dialogs.echo[LANG]),
                GifCommand('gif', dialogs.gif[LANG]),
                GoogleCommand('google', dialogs.google[LANG]),
                HelpCommand('help', dialogs.help[LANG]),
                PollCommand('poll', dialogs.poll[LANG]),
                PutinCommand('putin', dialogs.putin[LANG]),
                QuoteCommand('quote', dialogs.quote[LANG]),
                StatusCommand('status', dialogs.status[LANG]),
                WikiCommand('wiki', dialogs.wiki[LANG]),
                WeatherCommand('weather', dialogs.weather[LANG]),
                YouTubeCommand('youtube', dialogs.youtube[LANG])
               ]
