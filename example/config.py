from commands.bbq import BBQCommand
from commands.dice import DiceCommand
import dialogs

TOKEN = ''  # enter authorization token here
BOT_NAME = 'PyBot'   # enter name of the bot here
LANG = 'en'  # 'en' for english, 'nl' for dutch
COMMAND_LIST = [
		        BBQCommand('bbq', dialogs.bbq[LANG]),
                DiceCommand('dice', dialogs.dice[LANG])
			   ]
