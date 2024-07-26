from lib.core.specmodule import SpecModule


class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        Enumerates the installed Office Architecture on the host. 
        This module writes the result to agent in the database.
        It retrieves the bitness from the Path value under 
        HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths\\outlook.exe.

        It uses WbemScripting.SWbemLocator
        - ConnectServer(root\cimv2)
        - ConnectServer(root\cimv2).GetStringValue
        """
        self.entry = 'list_officearch'
        self.depends = []
        super().__init__(templatepath)
        
    def rethandler(self, agent, options, data):
        agent.officearch = data