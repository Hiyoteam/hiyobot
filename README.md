# Hiyobot
一个简单hack.chat机器人框架。    
If your native language is not Chinese, please jump [here](https://deepl.com/) .     
<img src="https://img.shields.io/badge/Powered%20By-Python-blue.svg"></img> <img src="https://img.shields.io/badge/Powered%20By-websocket_client-blue.svg"></img> <img src="https://img.shields.io/badge/Document%20version-0.0.2-green.svg"></img> <img src="https://img.shields.io/pypi/v/hiyobot"></img> <img src="https://github.com/Hiyoteam/hiyobot/actions/workflows/python-publish.yml/badge.svg"></img> <img src="https://static.pepy.tech/personalized-badge/hiyobot?period=total&units=international_system&left_color=grey&right_color=blue&left_text=pypi%20downloads"></img>  


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
暂无

# 注释
 - HiyoBot PYPI版本取决于Hack.chat子集版本。
 - HiyoBot子集使用： 如在Hack.chat编写机器人:`from hiyobot import hackchat as hcbot`, 在ZhangChat(chat.zhangsoft.eu.org or chat.zhangsoft.cf)编写机器人:`from hiyobot import zhangchat as zhcbot`
 - 目前支持的聊天室： Hack.chat(hackchat),ZhangChat(zhangchat)
 - 如其他子集使用方式与Hack.chat集不同，即开设子文档。（暂无）
 - 我们会始终欢迎您的PR/Issues！
