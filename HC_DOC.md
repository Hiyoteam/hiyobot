# Hiyobot Hack.chat 开发文档

## hackchat.Bot
### 描述
&emsp;此类创建一个Hackchat Hiyobot Bot实例。
### 参数
 - channel: 机器人要加入的频道。
 - nick: 机器人名称。
 - password: 机器人的密码。(可选)
 - joinoncreate: 布尔值，为True时在类创建时立刻加入频道(可选)
 - proxy: 使用代理，接受hackchat.Proxy类。(可选)
 - wsopts: 词典，将会序列化后传入websocket.create_connection (可选)
### 示例
```python
from hiyobot import hackchat as hc
bot1=hc.Bot("programming","awaBot") #在programming频道创建名为awaBot的机器人
bot2=hc.Bot("programming","awaBot","SomePassword") #在programming频道创建名为awaBot的机器人,密码为SomePassword
bot3=hc.Bot("programming","awaBot","SomePassword",joinoncreate=False) #在programming频道创建名为awaBot的机器人,密码为SomePassword,不要立刻加入频道
bot3.join() #让机器人加入频道
bot4=hc.Bot("programming","awaBot","SomePassword",proxy=hc.Proxy(url="socks4://11.4.51.4:11451")) #在programming频道创建名为awaBot的机器人,密码为SomePassword,使用代理socks4://11.4.51.4:11451

#wsopts在此不做演示
```

## @bot.on
### 描述
&emsp;创建一个机器人事件。（为装饰器）
### 参数
 - matcher: 此事件的触发器。
### 示例
```python
from hiyobot import hackchat as hc
bot=hc.Bot("programming","awaBot","SomePassword") #在programming频道创建名为awaBot的机器人,密码为SomePassword
@bot.on(hc.Matcher(lambda x:x.get("text") == "Hello")) #当有人发送内容为"Hello"的内容时
async def event(session,data): #构造事件处理器
    #session为此次会话
    #data为json包内容
    session.bot.send("Hello there!") #发送 Hello there!
bot.run() #进入事件主循环
```
### 注释
&emsp;Matcher为一个函数，用来匹配“此事件是否应该运行。”  
  
&emsp;推荐使用lambda函数来编写Matcher.示例：`hc.Matcher(lambda x:在这里写你的表达式，可以读取x的内容，x是收到的JSON)`

//@TODO: Finish docs