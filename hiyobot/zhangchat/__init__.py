import websocket,ssl,json,threading,uuid,time,logging,re,traceback,inspect,asyncio
from functools import wraps
HIYOBOT_VERSION=(0,2,3)
MAX_RECV_LOG_LIMIT=100 #0 for no limit
def _isasync(func):
    if inspect.isasyncgenfunction(func) or inspect.iscoroutinefunction(func):
        return True
    else:
        return False
class Bot:
    """
    Simple Hack.chat bot class.
    """
    def __init__(self,channel,nick,password=None,joinoncreate=True) -> None:
        """
        Init the Bot.
        """
        self.channel,self.nick,self.password=channel,nick,password
        self.events=[]
        self.checks=[]
        self.config={}
        if joinoncreate:
            self.join()
    def join(self):
        """
        Send the request that joining into the channel.
        """
        self.ws = websocket.create_connection("wss://chat.zhangsoft.eu.org/ws",sslopt={"cert_reqs":ssl.CERT_NONE})
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
                        check[1](check[2],session)
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
class Session:
    def __init__(self,bot,data):
        logging.debug(f"Built session(bot={bot})")
        self.bot=bot
        self.data=data
        self.extra_datas={}
        self.created_on=time.time()
        self.sessionID=str(uuid.uuid4())
    def wait_for_input(self,prompt=None,expires=60,delay=100):
        self.extra_datas["waitforinput"]=False
        if prompt:
            self.bot.send(prompt)
        #bind checker
        nick=self.data["nick"]
        checker=Matcher(Matchers.nick(nick))
        def check(session,newsession):
            #checked:
            logging.debug(f"Callback running: {session} and new one {newsession}")
            session.extra_datas["waitforinput"]=newsession.data.get("text")
        self.bot.checks.append((checker,check,self))
        stt=time.time()
        while (time.time()-stt)<expires:
            time.sleep(delay/1000)
            if self.extra_datas["waitforinput"]:
                logging.debug("Got message!")
                return self.extra_datas["waitforinput"]
        logging.debug("Session expired.")
        self.extra_datas["waitforinput"]=False
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


