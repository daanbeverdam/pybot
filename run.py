from core.pybot import PyBot
from etc import config
from etc import dialogs

if __name__ == "__main__":
    bot = PyBot(config.BOT_NAME, config.TOKEN, dialogs.bot[config.LANG],
                config.COMMAND_LIST, config.DATABASE)
    bot.run()
