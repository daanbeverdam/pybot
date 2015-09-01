from pybot.pybot import PyBot
import config

if __name__ == "__main__":
    bot = PyBot(config.BOT_NAME, config.TOKEN, config.COMMAND_LIST)
    bot.run()
