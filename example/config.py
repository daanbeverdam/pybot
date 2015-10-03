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
from commands.stats import StatsCommand
from commands.calculator import CalculatorCommand
from commands.hangman import HangmanCommand
from commands.xkcd import XKCDCommand
from commands.users import UsersCommand
from commands.marnie import MarnieCommand
import dialogs

# create a .txt file with your api token or alternatively,
# enter your authorization token here directly:
TOKEN = open('example/prefs.txt', 'r').readlines()[0].strip()
# enter name of the bot here:
BOT_NAME = open('example/prefs.txt', 'r').readlines()[1].strip()
# 'en' for english, 'nl' for dutch:
LANG = open('example/prefs.txt', 'r').readlines()[2].strip()
# commands can be removed or added:
COMMAND_LIST = [
                BBQCommand('bbq', dialogs.bbq[LANG]),
                CalculatorCommand('calculator', dialogs.calculator[LANG]),
                DiceCommand('dice', dialogs.dice[LANG]),
                DogeCommand('doge', dialogs.doge[LANG]),
                EchoCommand('echo', dialogs.echo[LANG]),
                GifCommand('gif', dialogs.gif[LANG]),
                GoogleCommand('google', dialogs.google[LANG]),
                HangmanCommand('hangman', dialogs.hangman[LANG]),
                HelpCommand('help', dialogs.help[LANG]),
                MarnieCommand('marnie', dialogs.marnie[LANG]),
                PollCommand('poll', dialogs.poll[LANG]),
                PutinCommand('putin', dialogs.putin[LANG]),
                QuoteCommand('quote', dialogs.quote[LANG]),
                StatsCommand('stats', dialogs.stats[LANG]),
                StatusCommand('status', dialogs.status[LANG]),
                UsersCommand('users', dialogs.users[LANG]),
                WikiCommand('wiki', dialogs.wiki[LANG]),
                WeatherCommand('weather', dialogs.weather[LANG]),
                XKCDCommand('xkcd', dialogs.xkcd[LANG]),
                YouTubeCommand('youtube', dialogs.youtube[LANG])
               ]
