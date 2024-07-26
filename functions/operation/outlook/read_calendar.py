from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring,makeint,makebool
from lib.validators.generic import ischoice
from lib.tab_completers.generic import tab_choice

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        This module allows you to read calendar items.

        It uses OutlookApplication
        - GetNameSpace("MAPI").GetDefaultFolder(9)
        - GetNameSpace("MAPI").GetDefaultFolder(9).items
        """
        self.entry = 'read_calendar'
        self.depends = []
        self.options['days_to_read'] = {
            "value": 7,
            "required": True,
            "description": "The number of days ahead of time you want to view the calendar for",
            "handler": makeint
        }
        self.options['include_body'] = {
            "value": "True",
            "required": True,
            "description": "List out the body of the meeting",
            "handler": makebool,
            "validator": ischoice,
            "validatorargs": {'choices': ["False", "True"]},
            "tab_complete": tab_choice,
            "tab_args": {'choices': ["False", "True"]}  
        }
        super().__init__(templatepath)