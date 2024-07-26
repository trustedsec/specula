from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring
import uuid

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        This module removes the registry keys that allows long running scripts such as list_dir running recurse or service acl enumeration. 

        The following value gets removed with this module:
        reg add "HKCU\Software\Microsoft\Internet Explorer\Styles" /v "MaxScriptStatements" /t REG_DWORD /d 0xFFFFFFFF /f

        It uses WbemScripting.SWbemLocator
        - ConnectServer(root\cimv2)
        - ConnectServer(root\cimv2).DeleteValue
        """
        self.entry = 'RemoveAllowLongScriptRuntime'
        self.depends = ['./helperFunctions/Delregvalue_hkcu.txt']
        
        super().__init__(templatepath)
