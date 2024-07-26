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

        It uses OutlookApplication
        - GetNameSpace("MAPI").GetDefaultFolder(VARIABLE)
        - GetNameSpace("MAPI").GetDefaultFolder(VARIABLE).items
        """
        self.entry = 'read_email'
        self.depends = []
        self.options['items_to_read'] = {
            "value": 10,
            "required": True,
            "description": "The number of items to read from the top (newest first)",
            "handler": makeint
        }
        self.options['folder_to_read_int'] = {
            "value": 1,
            "required": True,
            "description": "Folder you want to read emails from - Inbox, sent items etc",
            "handler": makeint,
            "hidden": True
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
            "description": "What folder to read emails from (system default folders - use options)",
            "handler": quotedstring,
            "validator": ischoice,
            "validatorargs": {'choices': ["inbox", "sent", "deleted", "drafts", "outbox", "junk", "Conversation History"]},
            "tab_complete": tab_choice,
            "tab_args": {'choices': ["inbox", "sent", "deleted", "drafts", "outbox", "junk", "Conversation History"]}
        }
        super().__init__(templatepath)

    def preprocess(self, agent):
    # Convert input to correct Integer needed for vbscript
        # https://docs.microsoft.com/en-us/office/vba/api/outlook.oldefaultfolders
        if self.options['folder_to_read']['value'] == "inbox":
            self.options['folder_to_read_int']['value'] = 6
        if self.options['folder_to_read']['value'] == "sent":
            self.options['folder_to_read_int']['value'] = 5
        if self.options['folder_to_read']['value'] == "outbox":
            self.options['folder_to_read_int']['value'] = 4
        if self.options['folder_to_read']['value'] == "deleted":
            self.options['folder_to_read_int']['value'] = 3
        if self.options['folder_to_read']['value'] == "drafts":
            self.options['folder_to_read_int']['value'] = 16
        if self.options['folder_to_read']['value'] == "junk":
            self.options['folder_to_read_int']['value'] = 23