from commands.putin import PutinCommand
from commands.bbq import BBQCommand
from commands.help import HelpCommand
from commands.dice import DiceCommand
from commands.doge import DogeCommand
from commands.gif import GifCommand

class Command():

    dictionary = {
        'bbq' : BBQCommand,
        # 'cancel' : CancelCommand,
        'dice' : DiceCommand,
        'doge' : DogeCommand,
        'gif' : GifCommand,
        # 'google' : GoogleCommand,
        'help' : HelpCommand,
        # 'krabbel' : KrabbelCommand,
        # 'laser' : LaserCommand,
        # 'poll' : PollCommand,
        'putin' : PutinCommand, 
        # 'request' : RequestCommand,
        # 'results' : ResultsCommand,
        # 'quote' : QuoteCommand,
        # 'status' : StatusCommand,
        # 'tips' : TipsCommand,
        # 'weather' : WeatherCommand,
        # 'wiki' : WikiCommand,
        # 'youtube' YoutubeCommand,  
    }

    def __init__(self, name, arguments = None):
        self.name = name
        self.arguments = arguments
        self.reply = self.get_reply()
        self.reply_type = self.get_reply_type()

    def get_reply(self):
        command = self.dictionary[self.name](self.arguments)
        reply = command.result
        return reply

    def get_reply_type(self):
        command = self.dictionary[self.name](self.arguments)
        return command.reply_type
