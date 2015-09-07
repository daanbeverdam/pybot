# PyBot
A Python framework for Telegram Bots
## How to Use
### Obtain API token from BotFather
The first step in running your own bot is getting an API token from Telegram. You do this by starting a Telegram conversation with @BotFather and sending it the '/newbot' command. Then just follow the directions you are given.
### Instructions for Mac OS & Linux
Some commands below need to be run with root privileges. Usually, putting `sudo` in front of the commands should do the trick.

Clone the git into a directory of choice:
```
git clone https://github.com/daanbeverdam/pybot.git
```
Then, open 'config.py' located in the example folder and find the line with `TOKEN =`. Now paste your previously obtained API token, replacing what is already there. It should look something like this:
```python
TOKEN = '123456789:ABCDEFGHIJKLMN_OPQRSTUVWXYZ'
```
Next, install the framework:
```
python pybot/setup.py install
```
And last, run the following command to start the bot:
```
python pybot/example/main.py
```
If everything is done right, your bot should now be up and running. Test it by starting a conversation and sending it '/status'.
### Instructions for Windows
PyBot has not been tested on Windows yet.
