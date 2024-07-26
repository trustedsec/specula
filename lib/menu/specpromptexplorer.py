
import os
import cmd
import copy
from pathlib import PureWindowsPath
import traceback
from datetime import datetime
from lib.core.setup import gconfig
from lib.core.helpers import Helpers
from lib.menu.specpromptmodule import SpecPromptModule
from lib.core.utility import TaskClass

class SpecPromptExplorer(cmd.Cmd):
    def __init__(self, selected_agent, helpers):
        self.ranAuto = False
        self.helpers = helpers
        self.selected_agent = selected_agent
        self.pathvar = PureWindowsPath("c:/")
        super().__init__()
        while len(self.helpers.rccommands) > 0:
            if self.onecmd(self.helpers.rccommands.pop(0)) is True:
                self.ranAuto = True
                return
    completekey = 'tab'

    def precmd(self, line): # Added for operator logging
        self.helpers.operatorlog(str("   "+line), False)
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
    
    def do_clear(self, inp):
        os.system('clear')
    
    def help_clear(self):
        print("Description: Clears the screen")
        print("Usage: clear")

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

    def do_pushnextcallback(self, inp):
        self.selected_agent.pushnextcallback = True
    
    def help_pushnextcallback(self):
        print("Description: Enables pushover notification on next callback from agent")

    def do_ls(self, inp):
        try:
            mod = self.helpers.get_module('operation/file/list_dir')
            mod.options['recurselevels']['value'] = "0"
            mod.options['filetype']['value'] = "*"
            mod.options['filename']['value'] = "*"
            mod.options['nodirectories']['value'] = "False"
            mod.options['nofiles']['value'] = "False"
            mod.options['sizeformat']['value'] = "mb"
            mod.options['output_console']['value'] = "True"
            mod.options['directory']['value'] = str(self.pathvar)
            task = TaskClass('operation/file/list_dir',
                             self.helpers.renderModule(mod, self.selected_agent),
                             mod.entry,
                             copy.deepcopy(mod.options),
                             True)
            self.selected_agent.add_task(task)
        except Exception as msg:
            print(" *** Error processing input: {}".format(msg))
    
    def help_ls(self):
        print("Description: List out directory and files from the current directory")
        print("Usage: ls")

    def do_cd(self, inp):
        try:
            if inp == "..":
                self.pathvar = PureWindowsPath(self.pathvar.parent)
            elif inp == "\\":
                self.pathvar = PureWindowsPath(self.pathvar.anchor)
            else:
                self.pathvar = PureWindowsPath(self.pathvar,inp)
        except Exception as msg:
            print(" *** Error processing input: {}".format(msg))
    
    def help_cd(self):
        print("Description: Change directory")
        print("Usage: cd temp")
        print("Usage: cd.. or cd ..")
        print("Usage: cd \\")

    def do_pwd(self, inp):
        try:
            print(str(self.pathvar))
        except Exception as msg:
            print(" *** Error processing input: {}".format(msg))
    
    def help_pwd(self):
        print("Description: Change directory")
        print("Usage: cd temp")
        print("Usage: cd..")

    def do_cat(self, inp):
        try:
            file = PureWindowsPath(self.pathvar,inp)
            mod = self.helpers.get_module('operation/file/cat_file')
            mod.options['file']['value'] = str(file)
            mod.options['output_console']['value'] = "True"
            task = TaskClass('operation/file/cat_file',
                             self.helpers.renderModule(mod, self.selected_agent),
                             mod.entry,
                             copy.deepcopy(mod.options),
                             True)
            self.selected_agent.add_task(task)
        except Exception as msg:
            print(" *** Error processing input: {}".format(msg))
    
    def help_cat(self):
        print("Description: Does Cat on the file to the screen. It uses the current path (pwd)+whatyoutype")
        print("Usage: cat file.txt")