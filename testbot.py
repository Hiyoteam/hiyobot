from time import sleep
from hiyobot import Bot,Matchers,Matcher,Utils,HIYOBOT_VERSION
bot=Bot("your-channel","TestBot","12345")
@bot.on(Matcher(Matchers.startswith("./ping")))
def on_message(data):
    bot.send("Pong!")
    @Utils.run_in_new_thread
    def _():
        sleep(5)
        bot.send(f"Pong! this message is sent by a new thread. also, with POWERFUL [HiyoBot](https://github.com/MaggieLOL/hiyobot) HCBot Framework Version {HIYOBOT_VERSION}!")
bot.run()