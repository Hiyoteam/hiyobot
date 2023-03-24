import websocket,ssl,json,threading
from functools import wraps
HIYOBOT_VERSION=(0,0,5)
class Bot:
    def __init__(self,channel,nick,password) -> None:
        self.ws = websocket.create_connection("wss://hack.chat/chat-ws",sslopt={"cert_reqs":ssl.CERT_NONE})
        self.ws.send(json.dumps({"cmd":"join","channel":channel,"nick":nick,"password":password}))
        self.events=[]
    def on(self,matcher):
        def decorate(func):
            @wraps(func)
            def wrapper(data,*args, **kwargs):
                if matcher.match_all(data):
                    return func(*args, **kwargs)
                else:
                    return None
            self.events.append(wrapper)
            return wrapper
        return decorate
    def send(self,data:dict|str):
        if type(data) == str:
            #auto-detect&convert type
            data=Message.Text(data)
        self.ws.send(json.dumps(data))
    def _run(self):
        while True:
            data = json.loads(self.ws.recv())
            for event in self.events:
                event(data,Data(data))
    def run(self,in_new_thread=False):
        if in_new_thread:
            self.thread=threading.Thread(target=self._run)
            self.thread.start()
        else:
            self._run()
class Matcher:
    def __init__(self,rule):
        self.rules=[]
        
        if rule == list:
            self.rules=list
        else:
            self.rules.append(rule)
    def add_rule(self,rule):
        self.rules.append(rule)
    def match(self,data):
        matched=False
        for rule in self.rules:
            matched_=rule(data)
            if matched_:
                matched=True
    def match_all(self,data):
        for rule in self.rules:
            matched=rule(data)
            if matched == False:
                return False
        return matched
class Data:
    def __init__(self,jsondata):
        for i in jsondata.items():
            self.__setattr__(i[0],i[1])
class Message:
    def Text(string):
        return {"cmd":"chat","text":string}
    def Image(URL):
        return {"cmd":"chat","text":f"![]({URL})"}
class Matchers:
    def message(data):
        return data["cmd"] == "chat"
    def join(data):
        return data["cmd"] == "onlineAdd"
    def startswith(text):
        def _startswith(data):
            return data.get("text","").startswith(text)
        return _startswith
class Utils:
    def in_new_thread(func):
        return lambda:threading.Thread(target=func).start()
    def run_in_new_thread(func):
        return threading.Thread(target=func).start()
