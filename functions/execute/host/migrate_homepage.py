from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring


class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        Migrate agent to another Specula server. 
        This module sets the URL to a new Specula server. 
        Useful in situations when you want to change host.
        It does NOT move the encrytion key so you must point to the validation url.
        !!Remember to have the other server up and running!!

        It uses WbemScripting.SWbemLocator
        - ConnectServer(root\cimv2)
        - ConnectServer(root\cimv2).CreateKey
        - ConnectServer(root\cimv2).SetStringValue
        - ConnectServer(root\cimv2).SetDWORDValue
        """
        self.entry = 'Execute_MigrateHomepage'
        self.depends = ['./helperFunctions/Setregvalue_hkcu.txt']
        self.options['homepageurl'] = {
            "value": None,
            "required": True,
            "description": "URL to new Specula Homepage validation",
            "handler": quotedstring
        }
        super().__init__(templatepath)
