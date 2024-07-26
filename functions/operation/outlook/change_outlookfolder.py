from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring,makeint,makebool
from lib.validators.generic import ischoice
from lib.tab_completers.generic import tab_choice

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        This module allows you to hide or unhide folders in outlook.
        Typical usecase is when you are about to send files using the
        sendfile_mail module you want to hide the outbox first.
        After all files are exfiled you can then unhide it.

        folder option should be set to int value found here: 
        https://docs.microsoft.com/en-us/office/vba/api/outlook.oldefaultfolders
        That means, 
        outbox would be 4
        inbox would be 6

        It uses OutlookApplication
        - GetNameSpace("MAPI").GetDefaultFolder(VARIABLE)
        - GetNameSpace("MAPI").GetDefaultFolder(VARIABLE).PropertyAccessor
        - GetNameSpace("MAPI").GetDefaultFolder(VARIABLE).PropertyAccessor.SetProperty
        """
        self.entry = 'change_outlookfolder'
        self.depends = []
        self.options['folder'] = {
            "value": None,
            "required": True,
            "description": "Folder to hide or unhide",
            "handler": makeint
        }
        self.options['hidden'] = {
            "value": False,
            "required": True,
            "description": "Set to True if you want to hide folder",
            "handler": makebool,
            "validator": ischoice,
            "validatorargs": {'choices': ["False", "True"]},
            "tab_complete": tab_choice,
            "tab_args": {'choices': ["False", "True"]}            
        }
        super().__init__(templatepath)
