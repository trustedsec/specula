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
from lib.core.specpayload import PayloadClass

class SpecPromptPayload(cmd.Cmd):
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
    
    def do_list(self, inp):
        print("list payloads in DB")

    def help_list(self):
        print("Description: Lists out all payloads imported into Specula")
        print("Usage: list")

    def do_remove(self, inp):
        try:
            if inp == "*":
                while 1:
                    confirm = input("Are you sure you want to delete all imported payloads from the database and disk?\n\nType YES to confirm (needs to be uppercase) - Anything else will exit without deleting\n")
                    if confirm == "YES":
                        print("Removed all imported payloads from DB and filesystem")
                        del self.helpers.p_list[:]
                        for file in os.scandir("./payloadhosting"):
                            os.remove(file.path)
                        self.helpers.save_payloads_to_file()
                        break
                    else:
                        break
            else:
                removepayload = self.helpers.p_list.get_payload_id(inp)
                self.helpers.p_list.remove_payload(removepayload)
                print("Removed imported payload from DB and filesystem")
                self.helpers.save_payloads_to_file()
        except ValueError:
            print("Something went wrong...Not sure what")
    

    
    def complete_remove(self, text, line, begidx, endidx):
        payload_ids = self.helpers.p_list.get_payloads_id()
        #print(payload_ids)
        return [i for i in payload_ids if i.startswith(text)]
        

    def help_remove(self):
        print("Description: use this to remove a payload from the DB and delete it from the payloadhosting folder")
        print("Usage: remove <payload id")

    def do_add(self, inp):
        try:
            args = Helpers.getarguments(inp)
            if len(args) == 0:
                print("You need to specify a path for a payload to add")
                return
            
            # Check if path leads to a file with a .extension
            if os.path.isfile(args[0]):
                if len(args) >= 2:
                    self.helpers.p_list.register_payload(args[0], args[1])    
                else:
                    self.helpers.p_list.register_payload(args[0], ''.join(random.choices(string.ascii_letters + string.digits, k=8)))
                print("Payload added for hosting")
            else:
                print("Path is not pointing to a file")
            self.helpers.save_payloads_to_file()
        except ValueError:
            print("Something went wrong...Not sure what")
    
    def complete_add(self, text, line, begidx, endidx):
        return [i for i in Helpers.complete_path(text,line) if i.startswith(text)]

    def do_list(self, inp):
        if self.helpers.p_list == []:
            print("No Payloads in Database")
        else:
            print("%-10s%-60s%-60s" % ("id","url","sourcepath"))
            for payload in self.helpers.p_list:
                print("%-10s%-60s%-60s" % (str(payload.id),str(payload.url),str(payload.sourcepath)))

    def help_add(self):
        print("Description: use this to add a payload to the DB and host it")
        print("Usage: add <path to payload>")
        print("Usage: add <path to payload> <name>")
    
    def help_clear(self):
        print("Description: Clears the screen")
        print("Usage: clear")
    
    def do_back(self, inp):
        return True

    def help_back(self):
        print("Description: Goes back in the menu")
        print("Usage: back")

    