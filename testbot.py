import hiyobot,time
bot=hiyobot.Bot("your-channel","TestBot","12345")
@bot.on(hiyobot.Matchers.startswith("./ping"))
def on_message(data):
    bot.send("Pong!")
    @hiyobot.Utils.run_in_new_thread
    def _():
        time.sleep(5)
        bot.send("Pong! this message is sent by a new thread.")
bot.run()