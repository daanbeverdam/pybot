# simple script used for importing an old log file into the database
from core.pybot import PyBot
from core.message import Message
from etc import config
from etc import dialogs
import json
import sys

if __name__ == "__main__":
    bot = PyBot(config.BOT_NAME, config.TOKEN, dialogs.bot[config.LANG],
                config.COMMAND_LIST, config.DATABASE)

    succeeded = 0
    failed = 0

    for arg in sys.argv[1:]:  # for every argument passed via the commandline

        print "Importing file " + arg + "..."

        try:
            log_entries = open(arg).readlines()

            for entry in log_entries:

                if entry[-2] == ',':
                    entry = entry[:-2]

                entry = json.loads(entry)

                if entry.get('message'):
                    message = Message(entry['message'])
                    bot.collect(message)
                    succeeded += 1
                else:
                    print "Skipping following entry because 'message' key could not be found:"
                    print entry, '\n'
                    failed += 1

                sys.stdout.write(str(failed + succeeded))
                sys.stdout.write('\b\b' * len(str(failed + succeeded)))
                sys.stdout.flush()

        except Exception, e:
            print "Something went wrong during import:"
            print e

    if len(sys.argv) < 2:
        print "No log file specified! Usage:\npython import.py /path/to/json.log"
    else:
        print "Succeeded:", succeeded
        print "Failed:", failed
        print "Total entries:", failed + succeeded
