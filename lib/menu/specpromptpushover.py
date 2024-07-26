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


class SpecPromptPushover(cmd.Cmd):
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
    
    def do_listpushoverkeys(self, inp):
        if gconfig.PUSHOVER_API_TOKEN != None:
            try:
                for value in gconfig.PUSHOVER_API_TOKEN.split(","):
                    print(value)
            except ValueError:
                print("Something went wrong...Not sure what")
        else:
            print("No pushover defined - List is empty")

    def help_listpushoverkeys(self):
        print("Description: Lists out all API Keys that will receive Push Notifications from Pushover")
        print("Usage: listpushoverkeys")

    def do_removepushoverkey(self, inp):
        try:
            args = Helpers.getarguments(inp)
            if len(args) == 0:
                print("You need to specify a key to remove")
                return
            token_list = gconfig.PUSHOVER_API_TOKEN.split(",") #Convert to list
            while inp in token_list: 
                token_list.remove(inp)
            setattr(gconfig, 'PUSHOVER_API_TOKEN', ",".join(token_list)) #convert back to string format and update the config file 
        except ValueError:
            print("Something went wrong...Not sure what")
    
    def complete_removepushoverkey(self, text, line, begidx, endidx):
        return [str(i) for i in gconfig.PUSHOVER_API_TOKEN.split(",") if str(i).startswith(text)]

    def help_removepushoverkey(self):
        print("Description: use this to remove one API Key from the config")
        print("Usage: removepushoverkey <apikey>")

    def do_addpushoverkey(self, inp):
        try:
            args = Helpers.getarguments(inp)
            if len(args) == 0:
                print("You need to specify a key to add")
                return
            if gconfig.PUSHOVER_API_TOKEN != None:
                token_list = gconfig.PUSHOVER_API_TOKEN.split(",") #Convert to list
                while inp not in token_list: 
                    token_list.append(inp)
                setattr(gconfig, 'PUSHOVER_API_TOKEN', ",".join(token_list)) #convert back to string format and update the config file 
            else:
                setattr(gconfig, 'PUSHOVER_API_TOKEN', inp)
        except ValueError:
            print("Something went wrong...Not sure what")
    
    def help_addpushoverkey(self):
        print("Description: use this to add one API Key to the config")
        print("Usage: addpushoverkey <apikey>")

    def do_testpush(self, cmd):
        self.helpers.sendPush("0.0.0.0", "test", cmd)
        print('Attempted to send push to pushover.net account using user token(s): {}'.format(gconfig.PUSHOVER_API_TOKEN))

    def help_testpush(self):
        print("Purpose: This attempt to send a message to the configured pushover_api_token(s) to verify configuration")
        print("Usage: testpush <message>")

    def do_subscriptions(self, inp):
        try:
            print("PUSH_VALIDATION - Push on Validation: " + str(gconfig.PUSH_VALIDATION))
            print("PUSH_NEWAGENT - Push on New Agent: " + str(gconfig.PUSH_NEWAGENT))
            print("PUSH_NEWIP - Push on New IP on Agent: " + str(gconfig.PUSH_NEWIP))
            print("PUSH_PRESTAGE - Push on Prestage Agent: " + str(gconfig.PUSH_PRESTAGE))
            print("PUSH_UNKNOWNCONNECTION - Push on Unknown Connection: " + str(gconfig.PUSH_UNKNOWNCONNECTION))
            print("PUSH_UNEXPECTEDCALLBACK - Push on Unexpected Callback: " + str(gconfig.PUSH_UNEXPECTEDCALLBACK))
            print("PUSH_CONNECTION_OUTSIDESPECULA - Push on Connection Outside Specula(URLS): " + str(gconfig.PUSH_CONNECTION_OUTSIDESPECULA))
        except ValueError:
            print("Something went wrong...Not sure what")

    def help_subscriptions(self):
        print("Description: Use to list out current subscription settings")
        print("Usage: subscriptions")

    def do_changesubscription(self, cmd):
        args = Helpers.getarguments(cmd)
        if len(args) == 0:
            print("You need to specify a value to edit")
            return
        key = args.pop(0)
        if getattr(gconfig, key).lower() == "true":
            setattr(gconfig, key, "False")
            print("{} changed to False".format(key))
        else:
            setattr(gconfig, key, "True")
            print("{} changed to True".format(key))

    def complete_changesubscription(self, text, line, begidx, endidx):
        options = ["PUSH_NEWAGENT", "PUSH_NEWIP", "PUSH_VALIDATION","PUSH_PRESTAGE","PUSH_UNKNOWNCONNECTION","PUSH_UNEXPECTEDCALLBACK","PUSH_CONNECTION_OUTSIDESPECULA"]
        if text:
            options = [option for option in options if option.startswith(text)]
        return options

    def help_changesubscription(self):
        print("Description: Change Subscriptions for Pushover notifications. It will swith true to false in the config")
        print("Usage: changesubscription PUSH_NEWIP")

    def help_clear(self):
        print("Description: Clears the screen")
        print("Usage: clear")
    
    def do_back(self, inp):
        return True

    def help_back(self):
        print("Description: Goes back in the menu")
        print("Usage: back")

