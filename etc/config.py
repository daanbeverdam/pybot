from commands.dice import DiceCommand
from commands.doge import DogeCommand
from commands.gif import GifCommand
from commands.echo import EchoCommand
from commands.results import ResultsCommand
from commands.wiki import WikiCommand
from commands.google import GoogleCommand
from commands.poll import PollCommand
from commands.help import HelpCommand
from commands.status import StatusCommand
from commands.weather import WeatherCommand
from commands.quote import QuoteCommand
from commands.stats import StatsCommand
from commands.start import StartCommand
from commands.kudos import KudosCommand
from commands.changes import ChangesCommand
from commands.say import SayCommand
import dialogs
import json

config = json.loads(open('etc/config.json').read())
# Edit the .env file or alternatively, enter your environment variables manually.
# telegram API token:
TOKEN = config['token']
# name of the bot:
BOT_NAME = config['name']
# 'en' for english, 'nl' for dutch:
LANG = config['language']
# database name:
DATABASE = config['database']
# chat id of the bot admin (optional):
ADMIN_CHAT_ID = config.get('admin_id')
# api key for Open Weather Map (optional):
WEATHER_API = config.get('weather_api')
# api key for Voicerss (optional):
SAY_API = config.get('say_api')
# list of commands:
COMMAND_LIST = [
    ChangesCommand('/changes', dialogs.changes[LANG]),
    DiceCommand('/dice', dialogs.dice[LANG]),
    DogeCommand('/doge', dialogs.doge[LANG], requires_arguments=True),
    EchoCommand('/echo', dialogs.echo[LANG], requires_arguments=True),
    GifCommand('/gif', dialogs.gif[LANG], requires_arguments=True),
    GoogleCommand('/google', dialogs.google[LANG], requires_arguments=True),
    HelpCommand('/help', dialogs.help[LANG]),
    KudosCommand('/kudos', dialogs.kudos[LANG], is_always_listening=True),
    PollCommand('/poll', dialogs.poll[LANG], True, ADMIN_CHAT_ID),
    QuoteCommand('/quote', dialogs.quote[LANG]),
    ResultsCommand('/results', dialogs.results[LANG]),
    SayCommand('/say', dialogs.say[LANG], True, language=LANG, api_key=SAY_API),
    StartCommand('/start', dialogs.start[LANG]),
    StatsCommand('/stats', dialogs.stats[LANG]),
    StatusCommand('/status', dialogs.status[LANG]),
    WikiCommand('/wiki', dialogs.wiki[LANG], requires_arguments=True),
    WeatherCommand('/weather', dialogs.weather[LANG], requires_arguments=True, api_key=WEATHER_API),
]
