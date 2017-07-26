from pybot.commands.dice import DiceCommand
from pybot.commands.echo import EchoCommand
from pybot.commands.results import ResultsCommand
from pybot.commands.wiki import WikiCommand
from pybot.commands.poll import PollCommand
from pybot.commands.help import HelpCommand
from pybot.commands.status import StatusCommand
from pybot.commands.weather import WeatherCommand
from pybot.commands.quote import QuoteCommand
from pybot.commands.stats import StatsCommand
from pybot.commands.start import StartCommand
from pybot.commands.kudos import KudosCommand
from pybot.commands.changes import ChangesCommand
from pybot.etc import dialogs
from pybot.env import ROOT_DIR
import json

config = json.loads(open(ROOT_DIR + '/etc/config.json').read())
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
    EchoCommand('/echo', dialogs.echo[LANG], requires_arguments=True),
    HelpCommand('/help', dialogs.help[LANG]),
    KudosCommand('/kudos', dialogs.kudos[LANG], is_always_listening=True),
    PollCommand('/poll', dialogs.poll[LANG], True, ADMIN_CHAT_ID),
    QuoteCommand('/quote', dialogs.quote[LANG]),
    ResultsCommand('/results', dialogs.results[LANG]),
    StartCommand('/start', dialogs.start[LANG]),
    StatsCommand('/stats', dialogs.stats[LANG]),
    StatusCommand('/status', dialogs.status[LANG]),
    WikiCommand('/wiki', dialogs.wiki[LANG], requires_arguments=True),
    WeatherCommand('/weather', dialogs.weather[LANG], requires_arguments=True, api_key=WEATHER_API),
]
