from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        This module terminates the process name you define using the process option. 
        Be careful, since it will kill all processes with that name. 
        Meaning if you define winword.exe it will kill all instances of winword.exe

        It uses WbemScripting.SWbemLocator
        - ConnectServer(root\cimv2)
        - Query: Select Name,ProcessId,ParentProcessId from Win32_Process Where Name = VARIABLE
        - Query.Terminate()
        
        """
        self.entry = 'KillProc_Name'
        self.depends = []
        self.options['process'] = {
            "value": None,
            "required": True,
            "description": "process name you want to kill, all instances will be killed",
            "handler": quotedstring
        }
        super().__init__(templatepath)
