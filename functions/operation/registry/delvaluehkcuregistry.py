from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        This module deletes registry key in the HKCU hive specified in the PathToKey option recursivly. 

        It uses WbemScripting.SWbemLocator
        - ConnectServer(root\cimv2)
        - ConnectServer(root\cimv2).DeleteValue
        """
        self.entry = 'DelValue_HKCU_Registry'
        self.depends = ['./helperFunctions/Delregvalue_hkcu.txt']
        self.options['PathToKey'] = {
            "value": None,
            "required": True,
            "description": "Path to the key you were the value is located. Example: Software\\EvilCorp\\subkey",
            "handler": quotedstring
        }
        self.options['Valuename'] = {
            "value": None,
            "required": True,
            "description": "Valuename to the value you would like to delete. Example: URL",
            "handler": quotedstring
        }
        super().__init__(templatepath)
