from commands.putin import PutinCommand
from commands.bbq import BBQCommand
from commands.dice import DiceCommand
from commands.doge import DogeCommand
from commands.gif import GifCommand
from commands.echo import EchoCommand
from commands.wiki import WikiCommand
from help import HelpCommand
import dialogs

TOKEN = ''  # enter authorization token here
BOT_NAME = 'PyBot'   # enter name of the bot here
LANG = 'nl'  # 'en' for english, 'nl' for dutch
COMMAND_LIST = [  #  commands can be removed or added as pleased
                BBQCommand('bbq', dialogs.bbq[LANG]),
                DiceCommand('dice', dialogs.dice[LANG]),
                DogeCommand('doge', dialogs.doge[LANG]),
                EchoCommand('echo', dialogs.echo[LANG]),
                GifCommand('gif', dialogs.gif[LANG]),
                HelpCommand('help', dialogs.help[LANG]),
                PutinCommand('putin', dialogs.putin[LANG]),
                WikiCommand('wiki', dialogs.wiki[LANG])
               ]
