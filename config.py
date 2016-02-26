from commands.dice import DiceCommand
from commands.doge import DogeCommand
from commands.gif import GifCommand
from commands.echo import EchoCommand
from commands.results import ResultsCommand
# from commands.wiki import WikiCommand
# from commands.youtube import YouTubeCommand
from commands.google import GoogleCommand
from commands.poll import PollCommand
from commands.help import HelpCommand
from commands.status import StatusCommand
# from commands.weather import WeatherCommand
from commands.quote import QuoteCommand
from commands.stats import StatsCommand
# from commands.calculator import CalculatorCommand
# from commands.hangman import HangmanCommand
# from commands.xkcd import XKCDCommand
# from commands.users import UsersCommand
from commands.start import StartCommand
from commands.kudos import KudosCommand
from commands.changes import ChangesCommand
# from commands.say import SayCommand
import dialogs
from pymongo import MongoClient  # for accessing the database

env = open('.env').readlines()
# Edit the .env file or alternatively, enter your environment variables manually.
# telegram API token:
TOKEN = env[0].strip()
# name of the bot:
BOT_NAME = env[1].strip()
# 'en' for english, 'nl' for dutch:
LANG = env[2].strip()
# database name:
DATABASE = env[3].strip()
# chat id of the bot admin (optional):
ADMIN_CHAT_ID = env[4].strip()
# api key for Open Weather Map:
WEATHER_API = env[5].strip()
# api key for Voicerss:
SAY_API = env[6].strip()
# list of commands:
COMMAND_LIST = [
    # CalculatorCommand('/calculator', dialogs.calculator[LANG]),
    ChangesCommand('/changes', dialogs.changes[LANG]),
    DiceCommand('/dice', dialogs.dice[LANG]),
    DogeCommand('/doge', dialogs.doge[LANG], requires_arguments=True),
    EchoCommand('/echo', dialogs.echo[LANG], requires_arguments=True),
    GifCommand('/gif', dialogs.gif[LANG], requires_arguments=True),
    GoogleCommand('/google', dialogs.google[LANG], False),
    # HangmanCommand('/hangman', dialogs.hangman[LANG]),
    HelpCommand('/help', dialogs.help[LANG]),
    KudosCommand('/kudos', dialogs.kudos[LANG], is_always_listening=True),
    PollCommand('/poll', dialogs.poll[LANG], True, ADMIN_CHAT_ID),
    QuoteCommand('/quote', dialogs.quote[LANG]),
    ResultsCommand('/results', dialogs.results[LANG]),
    # SayCommand('/say', dialogs.say[LANG], False, language=LANG, api_key=SAY_API),
    StartCommand('/start', dialogs.start[LANG]),
    StatsCommand('/stats', dialogs.stats[LANG]),
    StatusCommand('/status', dialogs.status[LANG]),
    # UsersCommand('/users', dialogs.users[LANG]),
    # WikiCommand('/wiki', dialogs.wiki[LANG], False),
    # WeatherCommand('/weather', dialogs.weather[LANG], False, api_key=WEATHER_API),
    # XKCDCommand('/xkcd', dialogs.xkcd[LANG]),
    # YouTubeCommand('/youtube', dialogs.youtube[LANG], False)
]
