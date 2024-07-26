import random
import secrets
import string
import os
import cmd
import base64
from datetime import datetime
from lib.core.setup import gconfig


class SpecPromptPrestage(cmd.Cmd):
    def __init__(self, helpers):
        self.ranAuto = False
        self.helpers = helpers
        super().__init__()
        while len(self.helpers.rccommands) > 0:
            if self.onecmd(self.helpers.rccommands.pop(0)) is True:
                self.ranAuto = True
                return
    completekey = 'tab'

    def precmd(self, line): # Added for operator logging
        self.helpers.operatorlog(str("  "+line), False)
        return(line)

    def emptyline(self):
        """Called when an empty line is entered in response to the prompt.

        If this method is not overridden, it repeats the last nonempty
        command entered.

        """
        if self.lastcmd:
            self.lastcmd = ""
            return self.onecmd('\n')
    
    def do_clear(self, inp):
        os.system('clear')
    
    def help_clear(self):
        print("Description: Clears the screen")
        print("Usage: clear")
    
    def do_back(self, inp):
        return True

    def help_back(self):
        print("Description: Goes back in the menu")
        print("Usage: back")

    def do_list(self, inp):
        prestage_list = self.helpers.a_list.get_prestaged_agents()
        if prestage_list == []:
            print("No Prestaged SpeculaC2 Agents.")
        else:
            print("%-25s%-70s%-70s" % ("encryptionkey","url","codeurl"))
            for agent in prestage_list:
                print("%-25s%-70s%-70s" % (agent.encryptionkey,agent.url,agent.codeurl))

    def help_list(self):
        print("Description: Lists out interesting data from all prestaged agents")
        print("Usage: list")

    def do_new(self, inp):
        try:
            if inp == '':
                remote_ip = "10.10.10.10"
                user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36" ##Random or ask
                username = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))
                computername = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(14))
                sessionid = base64.b64encode((username + "|" + computername).encode('utf-16le'))
                prestagetime = datetime(1194, 1, 1, 9, 4).strftime(gconfig.TIME_FORMAT)
                self.helpers.a_list.register_agent(sessionid, remote_ip, user_agent, prestagetime)
                agent = self.helpers.a_list[-1]
                agent.prestaged = True
                agent.approved = True
                agent.keysent = True
                agent.generate_com()
                agent.firstseen = prestagetime
                print("Encryptionkey: {}\tUrl:{}".format(agent.encryptionkey,agent.url))
            elif int(inp) > 0:
                for _ in range(int(inp)):
                    remote_ip = "10.10.10.10"
                    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36" ##Random or ask
                    username = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))
                    computername = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(14))
                    sessionid = base64.b64encode((username + "|" + computername).encode('utf-16le'))
                    prestagetime = datetime(1194, 1, 1, 9, 4).strftime(gconfig.TIME_FORMAT)
                    self.helpers.a_list.register_agent(sessionid, remote_ip, user_agent, prestagetime)
                    agent = self.helpers.a_list[-1]
                    agent.prestaged = True
                    agent.approved = True
                    agent.generate_com()
                    agent.firstseen = prestagetime
                    print("Encryptionkey: {}\tUrl:{}".format(agent.encryptionkey,agent.url))
            self.helpers.save_agents_to_file()
        except ValueError:
            print("Please provide a valid number or nothing at all to prestage one")

    def help_new(self):
        print("Description: Used to create one or more prestaged agents")
        print("Usage: prestage")
        print("Usage: prestage 10")

    def do_custom(self, inp):
        while 1:
            askurl = input("Enter rest of agent url you want:\n" + gconfig.DNS_NAME + gconfig.BASE_PATH_AGENT_COM)
            url = gconfig.DNS_NAME + gconfig.BASE_PATH_AGENT_COM + askurl
            askcodeurl = input("Enter rest of agent codeurl you want:\n" + gconfig.DNS_NAME + gconfig.BASE_PATH_AGENT_COM)
            codeurl = gconfig.DNS_NAME + gconfig.BASE_PATH_AGENT_COM + askcodeurl
            askcodeurl = input("Enter rest of agent support you want:\n" + gconfig.DNS_NAME + gconfig.BASE_PATH_AGENT_COM)
            supporturl = gconfig.DNS_NAME + gconfig.BASE_PATH_AGENT_COM + askcodeurl
            remote_ip = "10.10.10.10"
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36" ##Random or ask
            username = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))
            computername = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(14))
            sessionid = base64.b64encode((username + "|" + computername).encode('utf-16le'))
            prestagetime = datetime(1194, 1, 1, 9, 4).strftime(gconfig.TIME_FORMAT)
            self.helpers.a_list.register_agent(sessionid, remote_ip, user_agent, prestagetime)
            self.helpers.save_agents_to_file()
            agent = self.helpers.a_list[-1]
            agent.prestaged = True
            agent.approved = True
            agent.keysent = True
            agent.generate_customcom(url, codeurl, supporturl)
            print("Encryptionkey: {}\tUrl:{}".format(agent.encryptionkey,agent.url))
            break
    
    def do_dev(self, inp):
        while 1:
            devurl = gconfig.DNS_NAME + "/devcom/" + secrets.token_urlsafe(10)
            devcodeurl = gconfig.DNS_NAME + "/devcom/codeurl/" + secrets.token_urlsafe(10)
            devsupporturl = gconfig.DNS_NAME + "/devcom/support/" + secrets.token_urlsafe(10)
            remote_ip = "20.20.20.20"
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36" ##Random or ask
            username = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))
            computername = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(14))
            sessionid = base64.b64encode((username + "|" + computername).encode('utf-16le'))
            prestagetime = datetime(1194, 1, 1, 9, 4).strftime(gconfig.TIME_FORMAT)
            self.helpers.a_list.register_agent(sessionid, remote_ip, user_agent, prestagetime)
            self.helpers.save_agents_to_file()
            agent = self.helpers.a_list[-1]
            agent.prestaged = True
            agent.approved = True
            agent.keysent = True
            agent.generate_customcom(devurl, devcodeurl, devsupporturl)
            print("Encryptionkey: {}\tUrl:{}".format(agent.encryptionkey,agent.url))
            break
    
    def help_custom(self):
        print("Description: Used to create a custom prestage agent. Lets you define urls to use. \n\tUrl and Codeurl must not be set to the same!")
        print("Usage: custom")