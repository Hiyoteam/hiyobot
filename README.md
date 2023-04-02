# Hiyobot
一个简单hack.chat机器人框架。
English document? use [this](https://deepl.com/)
<img src="https://img.shields.io/badge/Powered%20By-Python-blue.svg"></img> <img src="https://img.shields.io/badge/Powered%20By-websocket_client-blue.svg"></img> <img src="https://img.shields.io/badge/Document%20version-0.0.2-green.svg"></img><img src="https://img.shields.io/pypi/v/hiyobot"></img><img src="https://github.com/Hiyoteam/hiyobot/actions/workflows/python-publish.yml/badge.svg"></img>

# 如何安装？
在你的控制台里面输入`pip3 install hiyobot --upgrade`，如果你使用镜像源，可能无法获取到最新的构建，需要加上`-i https://pypi.org/simple`的参数。输出应该是这样的：
```
Collecting hiyobot
  Downloading hiyobot-<version>-py3-none-any.whl (8.3 kB)
Requirement already satisfied: websocket-client in c:\users\administrator\appdata\local\programs\python\python310\lib\site-packages (from hiyobot) (1.3.2)
Installing collected packages: hiyobot
Successfully installed hiyobot-<version>
```
# 开发文档
## 你的第一个机器人！
hiyobot提供Bot()类来实现机器人，分别接受3个参数（2必须,1可选）
```python
from hiyobot import Bot
bot=Bot("your-channel","Hiyobot_Demo")
```
这些代码创建一个叫做Hiyobot_Demo的机器人，将其作为名称，加入your-channel频道。
如果代码正常运行，你应该能看见在频道里加入了一个这样的机器人。
## 第一个事件！
hiyobot根据事件绑定器来判断“这个事件该不该执行”。例如`Matcher(Matchers.startswith("你好"))`就是一个匹配器，根据hiyobot内嵌的匹配器模板来匹配一切由`你好`开头的消息。
hiyobot给事件传入两个参数：session(当前会话),data(事件触发数据)。
下面我们进一步完善机器人，加上功能：收到以`你好`开头的消息时回复`你好啊！`
```python
from hiyobot import Bot,Matcher,Matchers
bot=Bot("your-channel","Hiyobot_Demo")
@bot.on(Matcher(Matchers.startswith("你好")))
def hello(session,data):
  session.bot.send("你好啊！")
bot.run()
```
最后使用bot.run进入事件监听循环。  
在运行这个实例后，你会发现:`哦，干，这怎么是个死循环`
是因为我们没有对机器人自身的消息做出判断。
```python
from hiyobot import Bot,Matcher,Matchers
bot=Bot("your-channel","Hiyobot_Demo")
@bot.on(Matcher(Matchers.startswith("你好")))
def hello(session,data):
  if data.nick == session.bot.nick:
    return
  session.bot.send("你好啊！")

bot.run()
```
大功告成！
  
  
文档还在完善，所以**我知道你很急，但是你先别急**
