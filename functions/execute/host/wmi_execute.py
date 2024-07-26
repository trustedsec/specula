from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring


class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        This module executes the specified command in the command option using the objProcess.Create method in WMI.
        It also returns the process ID of the new process you created.

        It uses WbemScripting.SWbemLocator
        - ConnectServer(root\cimv2)
        - ConnectServer(root\cimv2).Get("Win32_ProcessStartup").SpawnInstance_()
        - ConnectServer(root\cimv2).Get("Win32_Process")
        """
        self.entry = 'Execute_WMICommand'
        self.depends = []
        self.options['command'] = {
            "value": None,
            "required": True,
            "description": "Command to execute via wmi Process Create",
            "handler": quotedstring
        }
        super().__init__(templatepath)