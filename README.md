# PyBot

### What is it?
A Telegram bot written in Python.

### How do I use it?
In order to use the provided example, please follow the steps below.

#### Obtain API token from BotFather
The first step in running your own bot is getting an API token from Telegram. You do this by starting a Telegram conversation with @BotFather and sending it the '/newbot' command. Then just follow the directions you are given.

#### Setu
Some of the commands below need to be run with root privileges. Usually, putting `sudo` in front of the commands should do the trick.

Clone the git into a directory of choice:
```
git clone https://github.com/daanbeverdam/pybot.git
```
Then, open 'etc/config.py' located in the etc folder and fill in the details like the API token:
```python
TOKEN = '123456789:ABCDEFGHIJKLMN_OPQRSTUVWXYZ'
```
Alternatively, you could create an .env file. Then navigate to the pybot folder and run 'run.py':
```
cd pybot
python run.py
```
If everything is done right, your bot should now be up and running. Have fun!.
