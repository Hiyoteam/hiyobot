# Hiyobot
A simple bot framework for Hack.chat.

<img src="https://img.shields.io/badge/Powered%20By-Python-blue.svg"></img> <img src="https://img.shields.io/badge/Powered%20By-websocket_client-blue.svg"></img> <img src="https://img.shields.io/badge/Document%20version-0.0.2-green.svg"></img><img src="https://img.shields.io/pypi/v/hiyobot"></img><img src="https://github.com/Hiyoteam/hiyobot/actions/workflows/python-publish.yml/badge.svg"></img>

# How to use
Execute `pip3 install hiyobot` on your console. in some case, it will be `pip`.The output should looks like:
```
Collecting hiyobot
  Downloading hiyobot-<version>-py3-none-any.whl (8.3 kB)
Requirement already satisfied: websocket-client in c:\users\administrator\appdata\local\programs\python\python310\lib\site-packages (from hiyobot) (1.3.2)
Installing collected packages: hiyobot
Successfully installed hiyobot-<version>
```
# Example Bot
```python
from time import sleep
from hiyobot import Bot,Matchers,Matcher,Utils,HIYOBOT_VERSION
bot=Bot("your-channel","TestBot","12345") #Channel,Bot-nick,Password(optional)
@bot.on(Matcher(Matchers.startswith("./ping"))) #Run when recived message that startswith "./ping"
def on_message(data):
    bot.send("Pong!") # Pong!
    @Utils.run_in_new_thread #Run following function in a new thread
    def _():
        sleep(5)
        bot.send(f"Pong! this message is sent by a new thread. also, with POWERFUL [HiyoBot](https://github.com/MaggieLOL/hiyobot) HCBot Framework Version {HIYOBOT_VERSION}!") # Pong#2
bot.run() #Enter the Bot mainloop
```