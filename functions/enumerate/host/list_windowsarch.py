from lib.core.specmodule import SpecModule


class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        Enumerates the Windows Architecture on the host. 
        This module writes the result to agent in the database.
        Arch value is found under:
        HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment - PROCESSOR_ARCHITECTURE.

        It uses WbemScripting.SWbemLocator
        - ConnectServer
        - ConnectServer(root\cimv2).GetStringValue
        """
        self.entry = 'list_windowsarch'
        self.depends = []
        super().__init__(templatepath)
        
    def rethandler(self, agent, options, data):
        agent.windowsarch = data