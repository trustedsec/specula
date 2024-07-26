from lib.core.specmodule import SpecModule


class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        Enumerates all the information from the Network login profile.
        Contains interesting information such as logon restrictions, logon scripts, number of logons and password age

        It uses WbemScripting.SWbemLocator
        - ConnectServer(root\cimv2)
        - Query: SELECT * FROM Win32_NetworkLoginProfile
        """
        self.entry = 'list_networklogon'
        self.depends = []
        super().__init__(templatepath)
        