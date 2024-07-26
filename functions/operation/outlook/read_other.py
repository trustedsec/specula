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
        self.entry = 'read_other'
        self.depends = []
        self.options['items_to_read'] = {
            "value": 10,
            "required": True,
            "description": "The number of items to read from the top (newest first)",
            "handler": makeint
        }
        self.options['folder_to_read_int'] = {
            "value": 13,
            "required": True,
            "description": "Folder you want to read items from - tasks, todos, notes, journal",
            "handler": makeint,
            "hidden": True
        }
        self.options['folder_to_read'] = {
            "value": "tasks",
            "required": True,
            "description": "What folder to read from",
            "handler": quotedstring,
            "validator": ischoice,
            "validatorargs": {'choices': ["tasks", "notes", "todo", "journal"]},
            "tab_complete": tab_choice,
            "tab_args": {'choices': ["tasks", "notes", "todo", "journal"]}
        }
        super().__init__(templatepath)

    def preprocess(self, agent):
        # Convert input to correct Integer needed for vbscript
        # https://docs.microsoft.com/en-us/office/vba/api/outlook.oldefaultfolders
        if self.options['folder_to_read']['value'] == "tasks":
            self.options['folder_to_read_int']['value'] = 13
        if self.options['folder_to_read']['value'] == "notes":
            self.options['folder_to_read_int']['value'] = 12
        if self.options['folder_to_read']['value'] == "todo":
            self.options['folder_to_read_int']['value'] = 28
        if self.options['folder_to_read']['value'] == "journal":
            self.options['folder_to_read_int']['value'] = 11