from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring,makebool
from lib.validators.generic import ischoice
from lib.tab_completers.generic import tab_choice

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        This module allows you to send email as the user.

        It uses OutlookApplication
        - CreateItem(0)
        """
        self.entry = 'send_mail'
        self.depends = []
        self.options['recipient'] = {
            "value": None,
            "required": True,
            "description": "Who to send the email to",
            "handler": quotedstring
        }
        self.options['subject'] = {
            "value": None,
            "required": True,
            "description": "Subject in the email",
            "handler": quotedstring
        }
        self.options['body'] = {
            "value": None,
            "required": True,
            "description": "Content inside the mail",
            "handler": quotedstring
        }
        self.options['delete_after_sent'] = {
            "value": "True",
            "required": True,
            "description": "Set to True if you want to delete mail after it is sent - Will not end up in deleted items",
            "handler": makebool,
            "validator": ischoice,
            "validatorargs": {'choices': ["False", "True"]},
            "tab_complete": tab_choice,
            "tab_args": {'choices': ["False", "True"]}            
        }
        super().__init__(templatepath)