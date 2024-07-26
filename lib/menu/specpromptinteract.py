
import os
import cmd
import traceback
from datetime import datetime
from lib.core.setup import gconfig
from lib.core.helpers import Helpers
from lib.menu.specpromptmodule import SpecPromptModule
from lib.menu.specpromptexplorer import SpecPromptExplorer
class SpecPromptInteract(cmd.Cmd):
    def __init__(self, selected_agent, helpers):
        self.ranAuto = False
        self.helpers = helpers
        self.selected_agent = selected_agent
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
    
    def do_back(self, inp):
        return True

    def help_back(self):
        print("Description: Goes back in the menu")
        print("Usage: back")
    
    def do_info(self, inp):
        outlist = {}
        try:
            for value in vars(self.selected_agent):
                if value == "encryptedvbsfunctions":
                    pass
                elif value == "tasks":
                    outlist.update( {"tasks in queue" : len(self.selected_agent.tasks) })
                else:
                    outlist.update( {value : str(vars(self.selected_agent)[value]) })
            for key,val in sorted(outlist.items()):
                print("{} : {}".format(key,val) , end="\n")
        except ValueError:
            print("Something went wrong...Not sure what")

    def help_info(self):
        print("Description: Lists out all agent properties")
        print("Usage: info")

    def do_clear(self, inp):
        os.system('clear')
    
    def help_clear(self):
        print("Description: Clears the screen")
        print("Usage: clear")

    def do_clearagentdata(self, inp):
        while 1:
            confirm = input("Are you sure you want to delete agentdata from:\n" + self.selected_agent.hostname + "\nYou will not be able to recover this data after you answer yes. \n\nYou have been WARNED!\n\nType YES to confirm (needs to be uppercase) - Anything else will exit without deleting\nThis will delete the content inside the txt file in the agent_data folder\n")
            if confirm == "YES":
                open("agent_data/" + self.selected_agent.hostname + ".txt", "w").close()
                break
            else:
                break
        return True
    
    def help_clearagentdata(self):
        print("Description: Deletes the agents data in the agentdata folder")
        print("Usage: clearagentdata")

    def do_delete(self, inp):
        while 1:
            confirm = input("Are you sure you want to delete:\n" + self.selected_agent.hostname + " " + self.selected_agent.username + " " + self.selected_agent.remoteip + "\n\nA PREFERRED WAY WOULD BE TO RUN THE TASK: Exe - Remove Homepage.\nYou will not be able to recover this agent after you answer yes. \n\nYou have been WARNED!\n\nType YES to confirm (needs to be uppercase) - Anything else will exit without deleting\nThis will not delete txt files in agent_data folder\n")
            if confirm == "YES":
                self.helpers.a_list.remove(self.selected_agent)
                self.helpers.save_agents_to_file()
                break
            else:
                break
        return True
    
    def help_delete(self):
        print("Description: Delete this agent completly from the database, will NOT delete data file in the agents_data folder")
        print("Usage: delete")

    def do_refreshtime(self, inp):
        try:
            self.selected_agent.refreshtime = int(inp)
            self.helpers.save_agents_to_file()
        except ValueError:
            print("Enter a digit value: 1-99999")
    
    def help_refreshtime(self):
        print("Description: Sets the refreshtime for the agent - specified in seconds")
        print("Usage: refreshtime 360")

    def do_jitter(self, inp):
        try:
            self.selected_agent.jitter = int(inp)
            self.helpers.save_agents_to_file()
        except ValueError:
            print("Enter a digit value: 1-99999")
    
    def help_jitter(self):
        print("Description: Sets the jitter for the agent - specified in seconds")
        print("Usage: jitter 360")

    def do_data(self, inp):
        try:
            print("\n*** Listing data for {}. ***".format(self.selected_agent.hostname))
            print(open('./agent_data/'+self.selected_agent.hostname+'.txt', "r").read())
        except FileNotFoundError:
            print("File with data not found - verify that ./agent_data/{}.txt exists".format(self.selected_agent.hostname))
    
    def help_data(self):
        print("Description: List out the data retrieved from the agent.")
        print("Usage: data")
    
    def do_qlist(self, inp):
        if len(self.selected_agent.tasks) == 0:
            print("Empty queue")
        else:
            for item in self.selected_agent.tasks:
                print("Queue Item #{}".format(self.selected_agent.tasks.index(item) +1))
                print("\tModule Name:\t{}".format(item.name))
                print("\tTime Added:\t{}".format(item.added))
                print("\tTime Passed:\t{}".format(datetime.strptime(datetime.now().strftime(gconfig.TIME_FORMAT), gconfig.TIME_FORMAT)-datetime.strptime(item.added,gconfig.TIME_FORMAT)))
                if hasattr(item, 'status'):
                    print("\tstatus:\t{}".format(item.status))
                for arg in item.options.keys():
                    if 'hidden' in item.options[arg] and item.options[arg]['hidden']:
                        continue
                    print("\t{}:\t{}".format(arg, item.options[arg]['value']))
                print("\n")
            print("Agent Last check-in: {}".format(self.selected_agent.lastcheckin))

    def help_qlist(self):
        print("Description: Lists out the current task queue for the agent")
        print("Usage: qlist")

    def do_qdel(self, inp):
        try:
            if inp == "*":
                print("Deleted all queued tasks")
                del self.selected_agent.tasks[:]
            else:
                inp = int(inp) - 1 #starts a 0, queue lists from 1
                print("Deleting {}".format(self.selected_agent.tasks[inp].name))
                self.selected_agent.tasks.pop(inp)
            self.helpers.save_agents_to_file()
        
        except SyntaxError:
            print("Not a valid number")
        
        except ValueError:
            print("Enter a digit or * to delete all tasks in queue - see help")

        except IndexError:
            print("Not a valid queue number - Use queue command to list")

    def help_qdel(self):
        print("Description: Delete either specified task by id or all by specifying *")
        print("Usage: qdel <id>")
        print("Usage: qdel *")

    def do_usemodule(self, inp):
        try:
            selected_module = self.helpers.get_module(inp)
            i = SpecPromptModule(self.helpers, selected_module, self.selected_agent, self.prompt[:-1]+':'+inp+'>')
            if i.ranAuto:
                return
            i.cmdloop()
        except KeyError:
            traceback.print_exc()
            print("Error - Did you type a valid module name?")
        except ValueError:
            traceback.print_exc()
            print("Error - Did you type a valid module name?")
        except TypeError:
            traceback.print_exc()
            print("Error - Did you type a valid module name?")
        except AttributeError:
            traceback.print_exc()
            print("Error - Did you type a valid module name?")


    def help_usemodule(self):
        print("Description: Interact with specified module")
        print("Usage: usemodule <modulename>")

    def do_explorer(self, inp):
        try:
            #agent = self.helpers.a_list.get_agent(int(inp))
            i = SpecPromptExplorer(self.selected_agent, self.helpers)
            if i.ranAuto:
                return
            i.prompt = self.prompt[:-1]+':'+self.selected_agent.hostname+':Explorer>'
            i.cmdloop()
        except KeyError:
            traceback.print_exc()
            print("Error - Did you type a valid module name?")
        except ValueError:
            traceback.print_exc()
            print("Error - Did you type a valid module name?")
        except TypeError:
            traceback.print_exc()
            print("Error - Did you type a valid module name?")
        except AttributeError:
            traceback.print_exc()
            print("Error - Did you type a valid module name?")


    def help_explorer(self):
        print("Description: Starts the explorer module")
        print("Usage: explorer")

    def do_pushnextcallback(self, inp):
        self.selected_agent.pushnextcallback = True
    
    def help_pushnextcallback(self):
        print("Description: Enables pushover notification on next callback from agent")

    def complete_usemodule(self, text, line, begidx, endidx):
        return [i for i in self.helpers.modlist.keys() if i.startswith(text)]

    def do_runTaskBook(self, cmd):
        try:
            if not (self.selected_agent.encryptionkey):
                print("Agent does not have an encryption key yet. Cannot queue tasks before it is a fully agent")
                return False
            task = self.helpers.taskbooks[cmd]
            task.TaskBook(self.helpers, self.selected_agent)
        except KeyError:
            traceback.print_exc()
            print("Error - Did you type a valid taskbook name?")
        except Exception as msg:
            traceback.print_exc()
            print("handled error running taskbook: {}".format(msg))

    def complete_runTaskBook(self, text, line, begidx, endidx):
        return [i for i in self.helpers.taskbooks.keys() if i.startswith(text)]

    def help_runTaskbook(self):
        print("Usage: runTaskbook <taskbookname>")