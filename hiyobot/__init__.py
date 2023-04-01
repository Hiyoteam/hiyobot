import websocket,ssl,json,threading,uuid,time,logging,re,traceback
from functools import wraps
HIYOBOT_VERSION=(0,1,3)
MAX_RECV_LOG_LIMIT=100 #0 for no limit
class Bot:
    def __init__(self,channel,nick,password=None) -> None:
        self.channel,self.nick,self.password=channel,nick,password
        self.events=[]
        self.checks=[]
        self.config={}
        self.join()
    def join(self):
        self.ws = websocket.create_connection("wss://hack.chat/chat-ws",sslopt={"cert_reqs":ssl.CERT_NONE})
        if self.password:
            self.ws.send(json.dumps({"cmd":"join","channel":self.channel,"nick":self.nick,"password":self.password}))
        else:
            self.ws.send(json.dumps({"cmd":"join","channel":self.channel,"nick":self.nick}))
    def on(self,matcher):
        def decorate(func):
            @wraps(func)
            def wrapper(session, data,*args, **kwargs):
                if matcher.match_all(data):
                    logging.debug(f"Matched! Function={func} Matcher={matcher}")
                    return func(session=session, data=data, *args, **kwargs)
                else:
                    return None
            self.events.append(wrapper)
            return wrapper
        return decorate
    def _bindRaw(self,function):
        self.events.append(function)
        logging.debug(f"Restigered Event-Function {function} for bot {self}")
    def load_plugin(self,plugin_name):
        #process the plugin name
        logging.debug("Ready for include module")
        plugin_name=plugin_name.replace("-","_")
        #import
        plugin=__import__(plugin_name)
        for command in plugin.exports:
            self._bindRaw(command)
        logging.debug(f"Included plugin {plugin_name}")
    def send(self,data:dict|str):
        if type(data) == str:
            #auto-detect&convert type
            data=Message.Text(data)
        self.ws.send(json.dumps(data))
        dumped=json.dumps(data)
        if MAX_RECV_LOG_LIMIT != 0:
            if len(dumped) >= MAX_RECV_LOG_LIMIT:
                logging.debug(f"Sent: {dumped[:MAX_RECV_LOG_LIMIT]}...")
            else:
                logging.debug(f"Sent: {dumped}")
        else:
            logging.debug(f"Sent: {dumped}")
    def _run(self,async_run=False):
        while True:
            data = json.loads(self.ws.recv())
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
    def run(self,async_mission=True,in_new_thread=False):
        if in_new_thread:
            self.thread=threading.Thread(target=self._run,args=(async_mission,))
            self.thread.start()
        else:
            self._run(async_mission)
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
        if type(data) == Data:
            data=data.__dict__
        for rule in self.rules:
            matched=rule(data)
            if matched == False:
                return False
        return matched
class Data:
    def __init__(self,jsondata):
        self.__dict__=jsondata
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
    def regex(text):
        def _regex(data):
            return bool(re.match(text,data.get("text","")))
        return _regex
    def nick(text):
        def _nick(data):
            return data.get("nick") == text
        return _nick
class Utils:
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
