from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring
import uuid

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        This module sets necessary registry keys to allow long running scripts such as list_dir running recurse or service acl enumeration. 

        The following value changes the default timeout for scripts running in Outlook and is being set with this module:
        reg add "HKCU\Software\Microsoft\Internet Explorer\Styles" /v "MaxScriptStatements" /t REG_DWORD /d 0xFFFFFFFF /f

        ! After setting this key, Outlook needs to be restarted for it to take effect !

        It uses WbemScripting.SWbemNamedValueSet
        - Add.__ProviderArchitecture

        It uses WbemScripting.SWbemLocator
        ConnectServer(root\cimv2)
        ConnectServer(root\cimv2).CreateKey
        ConnectServer(root\cimv2).SetDWORDValue
        """
        self.entry = 'AllowLongScriptRuntime'
        self.depends = ['./helperFunctions/Setregvalue_hkcu.txt']
        
        super().__init__(templatepath)
