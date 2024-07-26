from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring,makeint,makebool
from lib.validators.generic import ischoice
from lib.tab_completers.generic import tab_choice

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        This module allows you to read mail items.
        Specify the folder with folder_to_read.
        Format should be: inbox\\sublevel1\\sublevel2

        It uses OutlookApplication
        - Session.Folders(1).folders.item(FoldersArray(0)
        """
        self.entry = 'read_emailnamedfolder'
        self.depends = []
        self.options['items_to_read'] = {
            "value": 10,
            "required": True,
            "description": "The number of items to read from the top (newest first)",
            "handler": makeint
        }
        self.options['include_body'] = {
            "value": "True",
            "required": True,
            "description": "List out the body of the email",
            "handler": makebool,
            "validator": ischoice,
            "validatorargs": {'choices': ["False", "True"]},
            "tab_complete": tab_choice,
            "tab_args": {'choices': ["False", "True"]}  
        }
        self.options['folder_to_read'] = {
            "value": "inbox",
            "required": True,
            "description": "What folder (freetext) to read emails from - ex: inbox\\subfolder",
            "handler": quotedstring,
        }
        super().__init__(templatepath)
