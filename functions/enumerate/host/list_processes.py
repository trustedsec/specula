from lib.core.specmodule import SpecModule


class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        Enumerates running processes on the host. 
        It lists out:
        - PID
        - PPID
        - Arch based on virtual size (x86 set to less than 4094967296 Bytes, could be FP here) - Double check using operation-file-check_filearch
        - Process Name
        - Executable Path

        It uses WbemScripting.SWbemLocator
        - ConnectServer(root\cimv2)
        - Query: Select Name,ProcessId,ParentProcessId,VirtualSize,ExecutablePath from Win32_Process
        """
        self.entry = 'list_processes'
        self.depends = []
        super().__init__(templatepath)
        