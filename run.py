from pybot.core.bot import PyBot
from pybot.etc import config
from pybot.etc import dialogs

if __name__ == "__main__":
    bot = PyBot(config.BOT_NAME, config.TOKEN, dialogs.bot[config.LANG],
                config.COMMAND_LIST, config.DATABASE)
    bot.run()
