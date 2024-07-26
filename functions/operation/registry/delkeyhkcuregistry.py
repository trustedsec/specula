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
        - ConnectServer(root\cimv2).DeleteKey

        DeleteKey
        """
        self.entry = 'DelKey_HKCU_Registry'
        self.depends = ['./helperFunctions/Delregkey_hkcu.txt']
        self.options['PathToKey'] = {
            "value": None,
            "required": True,
            "description": "Path to the key you would like to delete. Example: Software\\EvilCorp\\subkey",
            "handler": quotedstring
        }
        super().__init__(templatepath)
