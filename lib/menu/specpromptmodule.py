import copy
import os
import cmd
import traceback

from lib.core.utility import TaskClass
from lib.core.helpers import Helpers

class SpecPromptModule(cmd.Cmd):
    def __init__(self, helpers, selected_module, selected_agent, prompt):
        self.ranAuto = False
        self.selected_module = selected_module
        self.selected_agent = selected_agent
        self.helpers = helpers
        self.prompt = prompt
        super().__init__()
        while len(self.helpers.rccommands) > 0:
            if self.onecmd(self.helpers.rccommands.pop(0)) is True:
                self.ranAuto = True
                return

    completekey = 'tab'

    def precmd(self, line): # Added for operator logging
        self.helpers.operatorlog(str("    "+line), False)
        return(line)

    #def preloop(self):
    #     #Define a task
    #     self.task = TaskClass(self.selected_module.name, self.selected_module.category, self.selected_module.subcat, self.selected_module.funcname, self.selected_module.args)
    #     self.do_options("display")
            # with open('random.txt', 'a') as file:
            # file.write('This is a line of text to append to the file.\n')

        

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

    def do_options(self, cmd):
        print("Module Help/Description: \n\t{}".format(self.selected_module.help))
        for k, v in self.selected_module.options.items():
            if 'hidden' in v and v['hidden'] is True:
                continue
            print("\n  {}\n\tValue: {}\n\tRequired: {}\n\tDescription: {}".format(k, v['value'], v['required'],
                                                                                  v['description']))
        print("\nUse set to change any presented options above.  If you do not see options, you can't configure this module")
        
    def help_options(self):
        print("Description: Shows the module options that are currently set")
        print("Usage: options")

    def do_set(self, cmd):
        """set PROFILE testprofile
        sets option for handler."""
        try:
            mykey = cmd.split(" ")[0].strip()
            myvalue = cmd.replace("%s " % (mykey), "")
            if mykey in list(self.selected_module.options.keys()):
                self.selected_module.set_option(mykey, myvalue)
            else:
                print(" *** Invalid value : %s" % (mykey))
        except Exception as msg:
            print(" *** Error processing input: {}".format(msg))

    def complete_set(self, text, line, start_index, end_index):
        arguments = self.helpers.getarguments(line)
        keylist = set(self.selected_module.options.keys())
        filter = set()
        for key in keylist:
            if 'hidden' in self.selected_module.options[key] and self.selected_module.options[key]['hidden'] is True:
                filter.add(key)
        keylist = list(keylist - filter)
        if len(arguments) > 1:
            arguments.pop(0)
        if arguments[0] in keylist:
            if 'tab_complete' in self.selected_module.options[arguments[0]]:
                args = {}
                if 'tab_args' in self.selected_module.options[arguments[0]]:
                    args = self.selected_module.options[arguments[0]]['tab_args']
                    if not isinstance(args, dict):
                        print(" *** tab_args for argument {} is invalid".format(arguments[0]))
                        args = {}
                return self.selected_module.options[arguments[0]]['tab_complete'](text, line, **args)
        else:
            if text:
                return [
                    name for name in keylist
                    if name.startswith(text)
                ]
            else:
                return keylist
    
    def help_set(self):
        print("Description: Allows you to set the different options for the module")
        print("Usage: set <option> <value>")

    def do_run(self, inp):
        try:
            if not (self.selected_agent.encryptionkey):
                print("Agent does not have an encryption key yet. Cannot queue tasks before it is a fully agent")
                return False
            task = TaskClass(self.prompt[self.prompt.rfind(':')+1:-1],
                             self.helpers.renderModule(self.selected_module, self.selected_agent),
                             self.selected_module.entry,
                             copy.deepcopy(self.selected_module.options),
                             False if inp == "False" or (hasattr(self.selected_module, "encrypt") and self.selected_module.encrypt is False) else True)
            self.selected_agent.add_task(task)
        except RuntimeError as msg:
            print('Unable to add Task, please correct Errors and try again')
            traceback.print_exc()
            return False
        print("Module {} added to execution queue".format(task.name))
        self.helpers.save_agents_to_file()
        return True

    def help_run(self):
        print("Description: Adds the module to the task queue for the agent and returns back to the agent context")
        print("Usage: run")
    
    def do_add(self, inp):
        try:
            if not (self.selected_agent.encryptionkey):
                print("Agent does not have an encryption key yet. Cannot queue tasks before it is a fully agent")
                return False
            task = TaskClass(self.prompt[self.prompt.rfind(':')+1:-1],
                             self.helpers.renderModule(self.selected_module, self.selected_agent),
                             self.selected_module.entry,
                             copy.deepcopy(self.selected_module.options),
                             False if inp == "False" or (hasattr(self.selected_module, "encrypt") and self.selected_module.encrypt is False) else True)
            self.selected_agent.add_task(task)
        except RuntimeError as msg:
            print('Unable to add Task, please correct Errors and try again')
            traceback.print_exc()
            return False
        print("Module {} added to execution queue".format(task.name))
        self.helpers.save_agents_to_file()
        return False
    
    def help_add(self):
        print("Description: Adds the module to the task queue for the agent but does not exit the menu context")
        print("Usage: add")
        
    def do_clear(self, inp):
        os.system('clear')
    
    def help_clear(self):
        print("Description: Clears the screen")
        print("Usage: clear")
