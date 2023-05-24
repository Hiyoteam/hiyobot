import hackchat
bot=hackchat.Bot("botest","aw22")
@bot.on(hackchat.Matcher(lambda x:x.get("text") == "awat"))
async def awat(session,data):
    session.bot.send(str(session.wait_for_input("awa!"))) 

bot.run()