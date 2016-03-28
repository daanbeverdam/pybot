# PyBot

### What is it?
A Telegram bot written in Python.

### How do I use it?
In order to use bot, please follow the steps below.

#### Obtain API token from BotFather
The first step is getting an API token from Telegram. You do this by starting a Telegram conversation with @BotFather and sending it the '/newbot' command. Then just follow the instructions.

#### Install MongoDB and PyMongo
The next step is installing [MongoDB](https://docs.mongodb.org/manual/installation/) and [PyMongo](https://api.mongodb.org/python/current/installation.html) on your machine, which allows the bot to store information into a database. Make sure a MongoDB instance is running before starting the bot.

#### Setup
Then, clone the repository into a directory of choice:
```
git clone https://github.com/daanbeverdam/pybot.git
```
Create a JSON file `etc/config.json` and fill in the details like the API token:
```JSON
{
"token": "123456789:ABCDEFGHIJKLMN_OPQRSTUVWXYZ",
"name": "MyBotName",
"language": "en",
"database": "database_name"
}
```
An example of a JSON config file can be found in the `etc` folder. Then navigate to the pybot folder and run `run.py`:
```
cd pybot
python run.py
```
Make sure the python program has write privileges so it can create the logfiles. If everything is done correctly, your bot should now be up and running. Have fun!
