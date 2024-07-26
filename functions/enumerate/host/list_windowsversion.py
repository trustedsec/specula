from lib.core.specmodule import SpecModule


class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        Enumerates the Current Windows version on the host.
        It retrieves data from HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion and lists out:
        - ProductName
        - ReleaseId

        It uses WbemScripting.SWbemLocator
        - ConnectServer
        - ConnectServer(root\cimv2).GetStringValue
        """
        self.entry = 'list_windowsversion'
        self.depends = []
        super().__init__(templatepath)
        
    def rethandler(self, agent, options, data):
        agent.windowsversion = data