from lib.core.specmodule import SpecModule
from datetime import datetime

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        Enumerates basic details about the host. It retrieves:
        - %Computername%
        - %Username%
        - %Userdomain%
        - %Userprofile%
        - %Userdnsdomain%
        - %Logonserver%
        - %Homepath%

        It uses Wscript.Shell
        - ExpandEnvironmentStrings
        """
        self.entry = 'list_basic'
        self.depends = []
        super().__init__(templatepath)

    def rethandler(self, agent, options, data):
        if ("-VSTO" not in agent.hostname): # Handle exception when VSTO agents are used
            agent.hostname = data.split()[3]
            agent.username = data.split()[1]

