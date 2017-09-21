# PyBot 🐍🤖

PyBot is a Telegram bot written in Python 3. I know, very original name. The bot is intended to be self-hosted and was specifically developed for group conversations with friends.

## What does it do?
\<feature showcase here\>

## How to run it?
Pybot should work on most \*NIX environments that have python 3 installed. There are a few package dependencies, which I might or might not list here in the future. Nothing major and you'll run into them anyway. 😉 In order to use bot, follow these steps.

### Obtain API token from BotFather
The first step is getting an API token from Telegram. You do this by starting a Telegram conversation with [@BotFather](https://telegram.me/botfather) and sending it the '/newbot' command. Then just follow the instructions.

### Installation
Clone the repository into a directory of choice.
```
git clone https://github.com/daanbeverdam/pybot.git
```
Navigate to the folder and install the package.
```
cd pybot/
python3 setup.py install
```
Create the JSON file `pybot/etc/config.json` and fill in the details. You should at least provide the API token, bot name and the language you want the bot to speak. For now, the options are English (`en`) and Dutch (`nl`). An example of config file can be found in the `etc` folder or take a look at the following.
```JSON
{
"token": "123456789:ABCDEFGHIJKLMN_OPQRSTUVWXYZ",
"name": "MyBotName",
"language": "en",
}
```
Now you can start the bot using the startup script.
```
python3 run.py
```
If everything is done correctly, your bot should now be up and running. Have fun!
