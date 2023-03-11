import hiyobot,threading,easygui,time
bot=hiyobot.Bot("your-channel","TestBot","12345")
@bot.on(hiyobot.Matchers.startswith("./ping"))
def on_message(data):
    bot.send(hiyobot.Message.Text("Pong!"))
bot.run(in_new_thread=True)