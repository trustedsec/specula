from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring,makebool
from lib.validators.generic import ischoice
from lib.tab_completers.generic import tab_choice


class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        Requires restart of Outlook to take effect after you have changed the settings.
        Set the different options to False to disable them.

        It uses WbemScripting.SWbemLocator
        - ConnectServer(root\cimv2)
        - ConnectServer(root\cimv2).CreateKey
        - ConnectServer(root\cimv2).SetStringValue
        - ConnectServer(root\cimv2).SetDWORDValue
        """
        self.entry = 'adjust_notifications'
        self.depends = ['./helperFunctions/Setregvalue_hkcu.txt']
        self.options['envelope'] = {
            "value": "True",
            "required": True,
            "description": "True enables envelope in taskbar on new email, False disables",
            "handler": makebool,
            "hidden": False,
            "validator": ischoice,
            "validatorargs": {'choices': ["False", "True"]},
            "tab_complete": tab_choice,
            "tab_args": {'choices': ["False", "True"]}         
        }
        self.options['sound'] = {
            "value": "True",
            "required": True,
            "description": "True enables sound on new email, False disables",
            "handler": makebool,
            "hidden": False,
            "validator": ischoice,
            "validatorargs": {'choices': ["False", "True"]},
            "tab_complete": tab_choice,
            "tab_args": {'choices': ["False", "True"]}         
        }
        self.options['toast'] = {
            "value": "True",
            "required": True,
            "description": "True enables toast popup on new email, False disables",
            "handler": makebool,
            "hidden": False,
            "validator": ischoice,
            "validatorargs": {'choices': ["False", "True"]},
            "tab_complete": tab_choice,
            "tab_args": {'choices': ["False", "True"]}         
        }
        super().__init__(templatepath)
    
    