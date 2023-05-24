import websocket,ssl,json,threading,uuid,time,logging,re,traceback,inspect,asyncio,queue
from functools import wraps
HIYOBOT_VERSION=(0,2,5)
MAX_RECV_LOG_LIMIT=100 #0 for no limit
def _isasync(func):
    if inspect.isasyncgenfunction(func) or inspect.iscoroutinefunction(func):
        return True
    else:
        return False
class Bot:
    """
    Simple ZhangChat bot class.
    """
    def __init__(self,channel,nick,password=None,joinoncreate=True,proxy=None,wsopts={}) -> None:
        """
        Init the Bot.
        """
        self.channel,self.nick,self.password=channel,nick,password
        self.events=[]
        self.checks=[]
        self.config={}
        self.proxy=proxy
        self.wsopts=wsopts
        if joinoncreate:
            self.join()
    def join(self):
        """
        Send the request that joining into the channel.
        """
        if not self.proxy:
            self.ws = websocket.create_connection("wss://chat.zhangsoft.cf/ws",sslopt={"cert_reqs":ssl.CERT_NONE},**self.wsopts)
        else:
            p=self.proxy.export()
            self.ws = websocket.create_connection("wss://chat.zhangsoft.cf/ws",sslopt={"cert_reqs":ssl.CERT_NONE},proxy_type=p[0],http_proxy_host=p[1],http_proxy_port=p[2],**self.wsopts)
        if self.password:
            self.ws.send(json.dumps({"cmd":"join","channel":self.channel,"nick":self.nick,"password":self.password,"bot":True,"client":"hiyooooooo"},ensure_ascii=False))
        else:
            self.ws.send(json.dumps({"cmd":"join","channel":self.channel,"nick":self.nick,"bot":True,"client":"hiyooooooo"},ensure_ascii=False))
    def on(self,matcher):
        """
        Add a new event.
        """
        def decorate(func):
            @wraps(func)
            def wrapper(session, data,*args, **kwargs):
                if matcher.match_all(data):
                    logging.debug(f"Matched! Function={func} Matcher={matcher}")
                    if _isasync(func):
                        return asyncio.run(func(session=session,data=data,*args,**kwargs))
                    else:
                        return func(session=session, data=data, *args, **kwargs)
                else:
                    return None
            self.events.append(wrapper)
            return wrapper
        return decorate
    def _pingThread(self):
        while 1:
            self.ws.send('{"cmd":"ping"}')
            time.sleep(60)
    def _bindRaw(self,function):
        self.events.append(function)
        logging.debug(f"Restigered Event-Function {function} for bot {self}")
    def load_plugin(self,plugin_name):
        """
        Load a Hiyobot Plugin.
        """
        #process the plugin name
        logging.debug("Ready for include module")
        plugin_name=plugin_name.replace("-","_")
        #import
        plugin=__import__(plugin_name)
        for command in plugin.exports:
            self._bindRaw(command)
        logging.debug(f"Included plugin {plugin_name}")
    def send(self,data):
        """
        Send JSON pack/text.
        """
        if type(data) == str:
            #auto-detect&convert type
            data=Message.Text(data)
        self.ws.send(json.dumps(data,ensure_ascii=False))
        dumped=json.dumps(data,ensure_ascii=False)
        if MAX_RECV_LOG_LIMIT != 0:
            if len(dumped) >= MAX_RECV_LOG_LIMIT:
                logging.debug(f"Sent: {dumped[:MAX_RECV_LOG_LIMIT]}...")
            else:
                logging.debug(f"Sent: {dumped}")
        else:
            logging.debug(f"Sent: {dumped}")
    def _run(self,async_run=False):
        while True:
            try:
                data = json.loads(self.ws.recv())
                
            except:
                logging.warning("Recv Data Failed, call re-join")
                self.join()
                continue
            def process(data):
                dumped=json.dumps(data)
                if MAX_RECV_LOG_LIMIT != 0:
                    if len(dumped) >= MAX_RECV_LOG_LIMIT:
                        logging.debug(f"Recv: {dumped[:MAX_RECV_LOG_LIMIT]}...")
                    else:
                        logging.debug(f"Recv: {dumped}")
                else:
                    logging.debug(f"Recv: {dumped}")
                session=Session(self,data)
                logging.debug(f"Matching Checks....")
                for check in self.checks:
                    if check[0].match_all(data):
                        logging.debug(f"Matched!")
                        check[1](Data(data),check[2],session)
                        self.checks.remove(check)
                    logging.debug(f"Skipping event matching because check has matched.")
                    continue
                logging.debug(f"Matching Event in {len(self.events)} Events...")
                for event in self.events:
                    try:
                        event(data=Data(data),session=session)
                    except Exception as e:
                        logging.warn(f"Error when processing Event {event}")
                        traceback.print_exc()
            if async_run:
                threading.Thread(target=process,args=(data,)).start()
            else:
                process(data)
    def run(self,async_mission=True,in_new_thread=False,ping_thread=True):
        """
        Enter the bot mainloop.
        """
        if in_new_thread:
            self.thread=threading.Thread(target=self._run,args=(async_mission,))
            self.thread.start()
        else:
            self._run(async_mission)
        if ping_thread:
            self.ping_thread=threading.Thread(target=self._pingThread)
            self.ping_thread.start()
class Matcher:
    """
    A class, to check "should this event run"
    """
    def __init__(self,rule):
        self.rules=[]
        
        if rule == list:
            self.rules=list
        else:
            self.rules.append(rule)
    def add_rule(self,rule):
        """
        Add a Checking function.
        """
        self.rules.append(rule)
    def match(self,data):
        """
        Match. if one is successed, then True
        """
        matched=False
        for rule in self.rules:
            matched_=rule(data)
            if matched_:
                matched=True
    def match_all(self,data):
        """
        Match. only return true when all function returns true
        """
        if type(data) == Data:
            data=data.__dict__
        for rule in self.rules:
            matched=rule(data)
            if matched == False:
                return False
        return matched
class Data:
    """
    Base Data Class
    """
    def __init__(self,jsondata):
        self.__dict__=jsondata
class Message:
    """
    Function-to-JSON class
    """
    def Text(string):
        return {"cmd":"chat","text":string,"head":""}
    def Image(URL):
        return {"cmd":"chat","text":f"![]({URL})"}
class Matchers:
    """
    Preset Matchers.
    """
    message=lambda x:x["cmd"] == "chat"
    join=lambda x:x["cmd"] == "onlineAdd"
    startswith=lambda x:lambda y:y.get("text","").startswith(x)
    regex=lambda x:lambda y:bool(re.match(x,y.get("text","")))
    nick=lambda x:lambda y:y.get("nick")==x
    nicknameTaken=lambda x:x["cmd"] == "warn" and x["text"] == "Nickname Taken"
class Utils:
    """
    Some tools.
    """
    def in_new_thread(func):
        return lambda:threading.Thread(target=func).start()
    def run_in_new_thread(func):
        return threading.Thread(target=func).start()
    
class Proxy:
    """
    Proxy Class.
    """
    def __init__(self,url=None,protocol=None,host=None,port=None):
        self.url=url
        self.host=host
        self.port=port
        self.protocol=protocol
        if url:
            self._explainURL()
    def _explainURL(self):
        url=self.url
        proto=url.split("://")[0]
        hp=url.split("://")[1].split(":")
        host=hp[0]
        port=int(hp[1])
        self.host=host
        self.port=port
        self.protocol=proto
    def export(self):
        return [self.protocol,self.host,self.port]
class Session:
    def __init__(self,bot,data):
        logging.debug(f"Built session(bot={bot})")
        self.bot=bot
        self.data=data
        self.extra_datas={}
        self.created_on=time.time()
        self.sessionID=str(uuid.uuid4())
    def wait_for_input(self,prompt=None,expires=60,checkrule=["chat","whisper"]):
        """
        Wait for user input, timeout in 60s.
        """
        if prompt:
            self.bot.send(prompt)
        #bind checker
        nick=self.data["nick"]
        checker=Matcher(lambda x:(x.get("cmd") == "chat" and x.get("nick") == nick) or (x.get("cmd") == "info" and x.get("type") == "whisper" and x.get("from") == nick) or (x.get("cmd") == "onlineRemove" and x.get("nick") == nick))
        callbackq=queue.Queue()
        def check(data,session,newsession):
            #checked:
            logging.debug(f"Callback running: {session} and new one {newsession}")
            if data.cmd == "onlineRemove":
                logging.debug("Target left, kill session.")
                callbackq.put([1]) #1=expire
                return
            
            #extract
            if data.cmd == "chat" and "chat" in checkrule:
                #public msg
                content=data.text
            elif data.cmd == "info" and "whisper" in checkrule:
                #private msg
                content=data.text.split(" 向你发送私信：",1)[1]
            else:
                #what the hell was that
                raise NotImplementedError("Unknown message type")
            callbackq.put([0,content,data])
        self.bot.checks.append((checker,check,self))
        try:
            data=callbackq.get(timeout=expires)
            if data[0] == 0:
                return data[1],data[2]
            if data[0] == 1:
                #what the hell was thatagain?
                raise NotImplementedError("Unknown callback status")
        except:
            logging.debug("Session expired.")
            raise TimeoutError("Session expired.")

class Plugin:
    def __init__(self):
        self.commands=[]
    def build_event(self,matcher):
        logging.debug(f"Built event for plugin {self}")
        def decorate(func):
            @wraps(func)
            def wrapper(session, data,*args, **kwargs):
                if matcher.match_all(data):
                    logging.debug(f"Matched! Function={func} Matcher={matcher}")
                    return func(session=session, data=data, *args, **kwargs)
                else:
                    return None
            self.commands.append(wrapper)
            return wrapper
        return decorate
    def build_exports(self):
        logging.debug(f"Built exports for plugin {self}")
        return self.commands
if __name__ == "__main__":
    raise Exception("Cannot run module as script!")


