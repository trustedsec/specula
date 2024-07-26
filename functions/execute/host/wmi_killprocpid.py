from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        This module terminates the process id you define using the pid option. 

        It uses WbemScripting.SWbemLocator
        - ConnectServer(root\cimv2)
        - Query: Select Name,ProcessId,ParentProcessId from Win32_Process Where ProcessID = VARIABLE
        - Query.Terminate()
        """
        self.entry = 'KillProc_PID'
        self.depends = []
        self.options['pid'] = {
            "value": None,
            "required": True,
            "description": "PID of the process you want to kill, all instances will be killed",
            "handler": quotedstring
        }
        super().__init__(templatepath)
