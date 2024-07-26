import secrets
import os
import base64
from collections import UserList
from datetime import datetime
from lib.core.setup import gconfig

class AgentListClass(UserList):
    def __init__(self):
        super().__init__()

    def get_agent(self, id):
        for agent in self:
            if int(agent.id) == int(id):
                return agent
        return None

    def get_agent_hostname(self, name):
        for agent in self:
            if agent.hostname == name:
                return agent
        return None

    def get_max_id(self):
        if self != []:
            id_list = []
            for agent in self:
                id_list.append(agent.id)
            return max(id_list)
        else:
            return int(0)

    def get_agents_id(self):
        id_list = []
        for agent in self:
                id_list.append(str(agent.id))
        return id_list

    def get_prestaged_agents(self):
        id_list = []
        for agent in self:
            if agent.prestaged:
                id_list.append(agent)
        return id_list
    
            #Agent version functions
    def register_agent(self, sessionid,remoteip,useragent,lastcheckin):
        hostname = base64.b64decode(sessionid).decode("utf-16le", "ignore").split("|")[0]
        username = base64.b64decode(sessionid).decode("utf-16le", "ignore").split("|")[1]

        newagent = AgentClass(sessionid, self.get_max_id()+1)
        newagent.hostname = hostname
        newagent.username = username
        newagent.useragent = useragent
        newagent.remoteip = remoteip
        newagent.lastcheckin = lastcheckin
        newagent.initialcheckincount = 0

        #Add to agent list
        self.append(newagent)


class AgentClass:
    def __init__(self, sessionid, myid):
        self.sessionid = sessionid  # instance variable unique to each instance
        self.hostname = None
        self.remoteip = None
        self.id = myid
        self.initialcheckincount = 0
        self.approved = False
        self.keysent = False
        self.api_verified = False
        self.api_installed = False
        self.tasks = []
        self.prestaged = False
        self.callback = 0
        self.encryptionkey = None
        self.url = None
        self.officearch = None
        self.windowsversion = None
        self.windowsarch = None
        self.sid = None
        self.timezone = None
        self.codeurl = None
        self.supporturl = None
        self.firstseen = datetime.now().strftime(gconfig.TIME_FORMAT)
        self.otherurls = {}
        self.pushnextcallback = False
        if not hasattr(self, 'refreshtime'):
            self.refreshtime = gconfig.DEFAULT_REFRESH_TIME
        if not hasattr(self, 'jitter'):
            self.jitter = gconfig.JITTER
        
    def generate_com(self):
        self.encryptionkey = secrets.token_urlsafe(16)
        self.url = gconfig.DNS_NAME + gconfig.BASE_PATH_AGENT_COM + secrets.token_urlsafe(10)
        self.codeurl = self.url + "/" + secrets.token_urlsafe(6)
        self.supporturl = self.url + "/" + secrets.token_urlsafe(5)
    
    def generate_customcom(self, url, codeurl, supporturl):
        self.encryptionkey = secrets.token_urlsafe(16)
        self.url = url
        self.codeurl = codeurl
        self.supporturl = supporturl
    
    def update_callback(self):
        self.callback += 1

    def updateinitialcheckincount(self, initialcheckincount):
        self.initialcheckincount = initialcheckincount

    def size_taskqueue(self):
        return len(self.tasks)

    def remove_task(self):
        self.tasks.pop(0)

    def add_task(self, item):
        self.tasks.insert(self.size_taskqueue(), item)
    
    def get_nexttask(self):
        return self.tasks[0]
