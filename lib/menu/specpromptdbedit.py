import random
import secrets
import string
import os
import cmd
import base64
import inspect
from datetime import datetime
from lib.core.setup import gconfig
from lib.core.helpers import Helpers


class SpecPromptDbedit(cmd.Cmd):
    def __init__(self, selected_agent, helpers):
        print("SHOULD ONLY BE USED FOR EDITING IF YOU KNOW WHAT YOU ARE DOING!")
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
    
    def do_list(self, inp):
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
    
    def help_list(self):
        print("Description: Lists out all agent properties")
        print("Usage: list")

    def do_set(self, cmd):
        args = Helpers.getarguments(cmd)
        if len(args) == 0:
            print("You need to specify a value to edit")
            return
        key = args.pop(0)
        if len(args) == 0:
            val = None
        else:
            val = ' '.join(args)
        try:
            if hasattr(self.selected_agent, key):
                setattr(self.selected_agent, key, val)
                print("{} Updated to {}".format(key,val))
            else:
                print("Invalid setting")
        except Exception as msg:
            print("Failed to set option: {}".format(msg))

    def help_set(self):
        print("Description: use this to change a setting")
        print("Usage: set <settingname> <value>")
        print("Should only be used if you know what you are doing\n"
              "Example: set refreshtime 100\n"
              "Example: set keysent False")


    def complete_set(self, text, line, begidx, endidx):
        return [i for i, j in inspect.getmembers(self.selected_agent) if i.startswith(text) and i[0] != '_']



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

