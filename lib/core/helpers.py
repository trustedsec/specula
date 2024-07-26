#should track agents
#should present agent add / remove for agents
import fnmatch
import os
import pickle
import copy
import random
import base64
import jinja2
import glob
import shlex
import json
import urllib.request as urllib2
from importlib import import_module
import datetime
from ipaddress import ip_network, ip_address
from lib.core.specagents import AgentListClass
from lib.core.specpayload import PayloadListClass
from lib.core.setup import gconfig
from lib.core.utility import TaskClass

class Helpers:
    def __init__(self, weblog): #DATABASEFILENAME
        self.logfile = open(gconfig.SPECULA_LOG_FILE, "a+")
        self.oplog = open(gconfig.OPERATOR_LOG_FILE, "a+")
        self.databasefilepath = gconfig.DATABASEFILENAME
        self.payloadsfilepath = gconfig.PAYLOADFILENAME
        self.basepath = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.logfilepath = gconfig.SPECULA_LOG_FILE
        self.timeformat = gconfig.TIME_FORMAT
        self.rccommands = []
        self.view_id = gconfig.OUTLOOK_VIEW_ID
        self.weblog = weblog
        self.a_list = AgentListClass()
        self.p_list = PayloadListClass()
        self.modlist = {}
        self.hiddenmods = {}
        self.taskbooks = {}
        self.completionlist = []
        self.Rand = random.Random()
        self.Rand.seed()
        self.blocklist = []
        self.allowlist = set() # items are added to the allowlist when they have been accepted once, blocklisting a allowlisted item will remove it from here
        if gconfig.IP_blocklist is not None:
            self.init_blocklist()

    @staticmethod
    def complete_path(path, line, **kwargs):
        if os.path.isdir(path):
            return glob.glob(os.path.join(path, '*'))
        else:
            return glob.glob(path + '*')

    def getpayloaddir(self):
        return os.path.join(self.basepath, "data/payloads")

    @staticmethod
    def getarguments(cmd):
        cmdparse = shlex.shlex(cmd, posix=True)
        cmdparse.escape = ''
        cmdparse.whitespace_split = True
        return list(iter(cmdparse))

    # inserts the configured module "module" into the provided agents task list
    # name must match what is found in the gui, otherwise callbacks will not function as expected
    def insertTask(self, agent, module, name):
        if name not in self.modlist:
            raise RuntimeError("name provided to insertTask is not found in the list of modules, must follow normal 'usemodule' format")
        task = TaskClass(name,
                         self.renderModule(module, agent),
                         module.entry,
                         copy.deepcopy(module.options),
                         True)
        agent.add_task(task)

    # helper to set a module option from for a taskbook
    @staticmethod
    def setModOption(mod, optname, optval=None, prompt="value: "):
        if optval is None:
            print('setting option {}'.format(optname))
            optval = input(prompt)
        while not mod.set_option(optname, optval):
            print('Invalid option given, try again')
            optval = input(prompt)



    def addJitter(self, jitter, time):
        round = int(time) + self.Rand.randint(0, int(jitter))
        return str(round)



    def sendPush(self, ip, hostname, msg):
        if(gconfig.PUSHOVER_API_TOKEN is None or gconfig.PUSHOVER_API_TOKEN == ""):
            return #don't send messages if you don't have someone to send them too
        if gconfig.PUSHOVER_APP_API_TOKEN is None:
            raise ValueError("Must update PUSHOVER_APP_API_TOKEN in config to use pushover")
        self.speclog("Push Msg {}:{} > {}".format(ip, hostname, msg))
        api_tokens = gconfig.PUSHOVER_API_TOKEN.split(",")
        for a_token in api_tokens:
            data = {"token": gconfig.PUSHOVER_APP_API_TOKEN,
                    "user": a_token,
                    "message": "{}:{}\n{}".format(ip, hostname, msg)}
            opener = urllib2.build_opener()
            try:
                req = urllib2.Request("https://api.pushover.net/1/messages.json", data=json.dumps(data).encode('utf-8'),
                                headers={'Content-Type': 'application/json'})
                urlout = opener.open(req)
                data = json.load(urlout)
                if data['status'] != 1:
                    print('Failed to send msg {}\n\nreason: {}'.format(msg, data['errors']))
                urlout.close()

            except urllib2.HTTPError as e:
                print("Failed to send pushover notification\nDouble check your pushover userkey and appkey in the config\nError code: {}".format(e.code))

    def renderModule(self, module, agent):
        if module.check_required() is False:
            return
        module.preprocess(agent)
        data = ""
        for item in module.depends: # append all expected dependency functions to top
            with open(item) as fp:
                data += "\n" + fp.read() + "\n"
        with open(module.templatepath) as fp:
            data += fp.read()
        with open('helperFunctions/base_template.txt') as fp:
            data += fp.read()
        env = jinja2.Environment(autoescape=False)
        doc = env.from_string(data)
        # module.postprocess(agent) to be readded in a better form later if needed
        context = {}
        values = [{k: module.get_option(k)} for k in module.options.keys()]
        for v in values:
            context.update(v)
        context.update({"OUTLOOK_VIEW_ID": gconfig.OUTLOOK_VIEW_ID,
                        "CALLBACKURL": agent.url,
                        "ENTRY": module.entry})
        return doc.render(context)

    @staticmethod
    def parseURI(uri):
        ssl = True if uri[:5].lower() == 'https' else False
        if uri.count(':') != 1:
            port = int(uri[uri.rfind(':') + 1:uri.find('/', 9)])
            host = uri[uri.find('//') + 2:uri.rfind(':')]
        else:
            port = 80 if not ssl else 443
            host = uri[uri.find('//') + 2:uri.find('/', 9)]
        path = uri[uri.find('/', 9):]
        return ssl, port, path, host

    def closelog(self): # this is only being used because tornado is a PITA for proper shutdown
        if self.logfile is not None:
            self.logfile.close()
            self.logfile = None

    def speclog(self, logline, output=False):
        msg = datetime.datetime.now().strftime(self.timeformat) + " - " + logline + "\n"
        self.logfile.write(msg)
        self.logfile.flush()
        if output:
            print(msg)

    def operatorlog(self, logline, output=False):
        msg = datetime.datetime.now().strftime(self.timeformat) + "\t" + logline + "\n"
        self.oplog.write(msg)
        self.oplog.flush()
        if output:
            print(msg)


    def get_module(self, p, hidden=False):
        mod = tmp = None
        if hidden:
            mod, tmp = self.hiddenmods[p]
        else:
            mod, tmp = self.modlist[p]
        module = mod.Spec(tmp, self)
        return module

    def loadTaskBooks(self, path):
        pattern = '*.py'
        for root, dirs, files in os.walk(path):
            for filename in fnmatch.filter(files, pattern):
                #  don't load up __init__
                if filename == "__init__.py":
                    continue
                filePath = os.path.join(root, filename)  # full path to our module
                modpath = filePath.replace('/', '.')[2:-3]
                # load the module
                mod = import_module(modpath)
                self.taskbooks[filePath[len('./Taskbooks/'):-3]] = mod

    #opens path and enumerates all paths to load modules
    def loadModules(self, path, hidden=False):
        pattern = '*.py'
        for root, dirs, files in os.walk(path):
            for filename in fnmatch.filter(files, pattern):
                #  don't load up __init__
                if filename == "__init__.py":
                    continue
                filePath = os.path.join(root, filename) #full path to our module
                name = filename[:-3]
                modpath = filePath.replace('/', '.')[2:-3]
                template = filePath[:-3] + ".txt"
                if not os.access(template, os.R_OK):
                    raise RuntimeError("Unable to read template associated with file {}".format(filePath))
                #load the module
                mod = (import_module(modpath), template)
                if hidden:
                    self.hiddenmods[filePath[len('./hiddenFunctions/'):-3]] = mod
                else:
                    self.modlist[filePath[len('./functions/'):-3]] = mod

    #static individual loader for hidden helper functions
    def loadModule(self, path):
        modpath = path.replace('/', '.')[2:-3]
        template = path[:-3] + ".txt"
        if not os.access(template, os.R_OK):
            raise RuntimeError("Unable to read template associated with file {}".format(path))
        # load the module
        print(modpath)
        print(template)
        mod = import_module(modpath)
        return mod.Spec(template, self)

    def save_agents_to_file(self, filename = None):
        _filename = filename if filename is not None else self.databasefilepath
        with open(_filename, "wb") as f:
            pickle.dump(self.a_list, f, pickle.HIGHEST_PROTOCOL)


    def load_agents_from_file(self, filename = None):
        _filename = filename if filename is not None else self.databasefilepath
        if os.path.exists(_filename):
            with open(_filename, "rb") as f:
                for agent in pickle.load(f):
                    self.a_list.append(agent)

    def save_payloads_to_file(self, filename = None):
        _filename = filename if filename is not None else self.payloadsfilepath
        with open(_filename, "wb") as f:
            pickle.dump(self.p_list, f, pickle.HIGHEST_PROTOCOL)


    def load_payloads_from_file(self, filename = None):
        _filename = filename if filename is not None else self.payloadsfilepath
        if os.path.exists(_filename):
            with open(_filename, "rb") as f:
                for agent in pickle.load(f):
                    self.p_list.append(agent)
                
    def init_blocklist(self):
        file = gconfig.IP_blocklist
        self.allowlist = set() # can be used as a re-init so we want to re zero these
        self.blocklist = []
        if os.access(file, os.R_OK):
            with open(file) as fp:
                self.blocklist = [ip_network(i.strip('\r\n'), strict=False) for i in fp.readlines()] #read all the lines, remove newlines they are all now networks
        else:
            # This can throw and we are intentionally letting it kill the system if it does
            with open(file, 'w') as fp: # create the blocklist file, we may update it later
                pass

    def listblocklist(self):
        if gconfig.IP_blocklist is None:
            print('blocklist currently disabled, to enable set IP_blocklist in the settings')
        else:
            print('blocklisted networks and IP\'s')
            for net in self.blocklist:
                print('\t{}'.format(net))

    def listallowlist(self):
        if gconfig.IP_blocklist is None:
            print('blocklist is currently disabled, ignoring allowlist')
            print('set IP_blocklist to a file to enable blocklist')
        else:
            print('current items in allowlist')
            for i in self.allowlist:
                print("\t{}".format(i))

    def addblocklist(self, ip, auto=True):
        if '/' in ip:
            print('''this interface does not support CIDR blocklist adds
            please add your CIDR range to the IP_blocklist file and then restart specula''')
            return
        if gconfig.IP_blocklist is None:
            if not auto:
                print('blocklist is currently disabled because the config option is not set. Please set IP_blocklist\n'
                      'then try again')
            return
        else:
            #next lets validate its not already covered by a blocklist range
            if not self.inblocklist(ip):
                try:
                    self.blocklist.append(ip_network(ip, strict=False))
                    with open(gconfig.IP_blocklist, 'a') as fp:
                        fp.write('\n' + ip)
                except Exception as msg:
                    print('failed to add ip to blocklist: {}'.format(msg))
            #We do this after because if it wasn't in the blocklist it'll be added when we check
            if ip in self.allowlist:
                self.allowlist.remove(ip)


    """Checks if a given ip is in the blocklist, returns TRUE if it is, else False"""
    def inblocklist(self, ip):
        ipaddr = None
        if gconfig.IP_blocklist is None or ip in self.allowlist:  # quick out for known good hosts / disabled blocklist
            return False
        try:
            ipaddr = ip_address(ip)
        except Exception as msg:
            print("Invalid ip when checking blocklist: {}".format(msg))
        for net in self.blocklist:
            if ipaddr in net:
                return True
        self.allowlist.add(ip)
        return False

    def pastenddate(self):
        if gconfig.END_DATE is None:
            return False
        else:
            if datetime.date.today() >= gconfig.END_DATE:
                return True
            return False






