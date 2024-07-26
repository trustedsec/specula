from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring,makebool
from lib.validators.generic import ischoice
from lib.tab_completers.generic import tab_choice

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        This module will delete mails in inbox and deleted items by default.
        If you set the delete_sent_items option to true it will look for mails in the sent items
        folder where your sender option is in the to field (mails sent from user to you)

        It uses OutlookApplication
        - GetNameSpace("MAPI").GetDefaultFolder(VARIABLE)
        - GetNameSpace("MAPI").GetDefaultFolder(VARIABLE).Items
        - GetNameSpace("MAPI").GetDefaultFolder(VARIABLE).Items().Delete
        """
        self.entry = 'delete_mail'
        self.depends = []
        self.options['sender'] = {
            "value": None,
            "required": True,
            "description": "Mails you want to delete sent from (your attacker mail address)",
            "handler": quotedstring
        }
        self.options['delete_sent_items'] = {
            "value": "False",
            "required": True,
            "description": "Set to True if you want to delete items in sent folder",
            "handler": makebool,
            "validator": ischoice,
            "validatorargs": {'choices': ["False", "True"]},
            "tab_complete": tab_choice,
            "tab_args": {'choices': ["False", "True"]}            
        }
        self.options['delete_permanent'] = {
            "value": "True",
            "required": True,
            "description": "True means nuking mails from deleted items after deleting from inbox and sent items",
            "handler": makebool,
            "validator": ischoice,
            "validatorargs": {'choices': ["False", "True"]},
            "tab_complete": tab_choice,
            "tab_args": {'choices': ["False", "True"]}            
        }
        super().__init__(templatepath)
