from time import sleep
from hiyobot import Bot,Matchers,Matcher,Utils
bot=Bot("your-channel","TestBot","12345")
@bot.on(Matcher(Matchers.startswith("./ping")))
def on_message(data):
    bot.send("Pong!")
    @Utils.run_in_new_thread
    def _():
        sleep(5)
        bot.send("Pong! this message is sent by a new thread.")
bot.run()