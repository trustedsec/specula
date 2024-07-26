from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring

class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        Whoami with limited information. Missing privileges since there is no way to get 
        that without API access or running external binaries

        It uses CreateObject("Wscript.Shell")
        It uses WbemScripting.SWbemLocator
        - ConnectServer(root\directory\LDAP)
        - Query: "SELECT DS_memberOf FROM ds_user Where DS_sAMAccountName = '" & strUsername & "'"

        - ConnectServer(root\cimv2)
        - Query: "SELECT * FROM Win32_UserProfile Where SID='" & strSID & "'"
        """
        self.entry = 'list_whoami'
        self.depends = []
        super().__init__(templatepath)

    def rethandler(self, agent, options, data):
        for line in data.split("\n"):
            if line.startswith("SID:"):
                sid = line.split()[1]
                if sid:
                    agent.sid = sid