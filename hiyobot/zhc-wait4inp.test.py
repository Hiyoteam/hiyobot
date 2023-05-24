import zhangchat,os
bot=zhangchat.Bot("chat","hiyotest",os.getenv("zhc_password"))
@bot.on(zhangchat.Matcher(lambda x:x.get("text") == "awat"))
async def awat(session,data):
    session.bot.send(str(session.wait_for_input("awa!"))) 

bot.run()